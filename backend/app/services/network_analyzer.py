"""
Network Analysis Service

Provides network connectivity analysis, switching path identification,
and customer impact assessment.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any, Optional, Set
from uuid import UUID
from collections import deque

from app import models


class NetworkAnalyzer:
    """Service for analyzing network topology and connectivity."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_connectivity(
        self,
        node_id: UUID,
        max_depth: int = 5
    ) -> Dict[str, Any]:
        """
        Analyze network connectivity from a given node using BFS.
        """
        # Verify node exists
        start_node = self.db.query(models.NetworkNode).filter(
            models.NetworkNode.id == node_id
        ).first()
        
        if not start_node:
            raise ValueError(f"Node {node_id} not found")
        
        # BFS to find connected nodes
        visited = {node_id}
        queue = deque([(node_id, 0)])
        connected_nodes = []
        
        while queue:
            current_id, depth = queue.popleft()
            
            if depth >= max_depth:
                continue
            
            # Find edges from this node
            edges = self.db.query(models.NetworkEdge).filter(
                models.NetworkEdge.from_node_id == current_id
            ).all()
            
            for edge in edges:
                if edge.to_node_id not in visited:
                    visited.add(edge.to_node_id)
                    queue.append((edge.to_node_id, depth + 1))
                    
                    # Get node details
                    node = self.db.query(models.NetworkNode).filter(
                        models.NetworkNode.id == edge.to_node_id
                    ).first()
                    
                    if node:
                        connected_nodes.append({
                            "node_id": node.id,
                            "name": node.name,
                            "type": node.node_type,
                            "voltage_level": node.voltage_level,
                            "distance": depth + 1
                        })
        
        # Count customers at risk
        customers_at_risk = self._count_customers_in_subgraph(visited)
        
        return {
            "node_id": node_id,
            "node_name": start_node.name,
            "analysis_type": "connectivity",
            "connected_nodes": connected_nodes,
            "total_connected": len(connected_nodes),
            "customers_at_risk": customers_at_risk["customers"],
            "load_at_risk_mw": customers_at_risk["load_mw"]
        }
    
    def analyze_switching_paths(
        self,
        node_id: UUID
    ) -> Dict[str, Any]:
        """
        Analyze available switching paths for a node.
        """
        # Get switching paths
        paths = self.db.query(models.SwitchingPath).filter(
            models.SwitchingPath.source_node_id == node_id,
            models.SwitchingPath.is_active == True
        ).all()
        
        switching_options = []
        for path in paths:
            target_node = self.db.query(models.NetworkNode).filter(
                models.NetworkNode.id == path.target_node_id
            ).first()
            
            switching_options.append({
                "path_id": path.id,
                "target_node_id": path.target_node_id,
                "target_node_name": target_node.name if target_node else None,
                "path_distance_km": float(path.path_distance_km) if path.path_distance_km else None,
                "switching_time_min": path.switching_time_min,
                "backup_capacity_mva": float(path.backup_capacity_mva) if path.backup_capacity_mva else None,
                "automatic_switching": path.automatic_switching
            })
        
        return {
            "node_id": node_id,
            "analysis_type": "switching_paths",
            "connected_nodes": [],
            "switching_options": switching_options,
            "total_paths": len(switching_options)
        }
    
    def analyze_load_flow(
        self,
        node_id: UUID
    ) -> Dict[str, Any]:
        """
        Analyze load flow from a node to identify downstream load.
        """
        # Get connected assets
        connected_assets = self._get_downstream_assets(node_id)
        
        total_load_mw = 0.0
        total_customers = 0
        
        for asset_id in connected_assets:
            conn = self.db.query(models.CustomerConnection).filter(
                models.CustomerConnection.asset_id == asset_id
            ).first()
            
            if conn:
                total_load_mw += float(conn.peak_load_mw or 0)
                total_customers += conn.customers_served or 0
        
        return {
            "node_id": node_id,
            "analysis_type": "load_flow",
            "connected_nodes": [],
            "downstream_assets": len(connected_assets),
            "customers_at_risk": total_customers,
            "load_at_risk_mw": total_load_mw
        }
    
    def get_downstream_customers(
        self,
        asset_id: UUID
    ) -> Dict[str, Any]:
        """
        Get all customers downstream of a given asset.
        """
        # Find the node associated with this asset
        node = self.db.query(models.NetworkNode).filter(
            models.NetworkNode.asset_id == asset_id
        ).first()
        
        if not node:
            return {
                "asset_id": asset_id,
                "direct_customers": 0,
                "downstream_customers": 0,
                "total_customers": 0
            }
        
        # Get direct customers
        direct_conn = self.db.query(models.CustomerConnection).filter(
            models.CustomerConnection.asset_id == asset_id
        ).first()
        
        direct_customers = direct_conn.customers_served if direct_conn else 0
        
        # Get downstream customers
        downstream_assets = self._get_downstream_assets(node.id)
        downstream_customers = 0
        
        for downstream_asset_id in downstream_assets:
            if downstream_asset_id == asset_id:
                continue
            
            conn = self.db.query(models.CustomerConnection).filter(
                models.CustomerConnection.asset_id == downstream_asset_id
            ).first()
            
            if conn:
                downstream_customers += conn.customers_served or 0
        
        return {
            "asset_id": asset_id,
            "node_id": node.id,
            "node_name": node.name,
            "direct_customers": direct_customers,
            "downstream_customers": downstream_customers,
            "total_customers": direct_customers + downstream_customers,
            "critical_facilities": {
                "hospitals": direct_conn.hospitals_served if direct_conn else 0,
                "schools": direct_conn.schools_served if direct_conn else 0,
                "emergency_services": direct_conn.emergency_services if direct_conn else 0
            } if direct_conn else {}
        }
    
    def identify_critical_paths(self) -> List[Dict[str, Any]]:
        """
        Identify critical paths in the network based on customer impact.
        """
        # Get all edges with their customer impact
        result = self.db.execute(text("""
            SELECT 
                ne.id as edge_id,
                ne.from_node_id,
                ne.to_node_id,
                ne.edge_type,
                ne.thermal_rating_mva,
                fn.name as from_node_name,
                tn.name as to_node_name,
                fn.asset_id as from_asset_id,
                tn.asset_id as to_asset_id
            FROM network_edges ne
            JOIN network_nodes fn ON ne.from_node_id = fn.id
            JOIN network_nodes tn ON ne.to_node_id = tn.id
        """))
        
        critical_paths = []
        
        for row in result:
            # Count downstream customers
            downstream_customers = 0
            downstream_load = 0.0
            
            if row.to_asset_id:
                downstream = self.get_downstream_customers(row.to_asset_id)
                downstream_customers = downstream["total_customers"]
            
            # Calculate criticality score
            criticality_score = downstream_customers / 1000.0  # Normalize
            
            if downstream_customers > 10000:  # Only include high-impact paths
                critical_paths.append({
                    "edge_id": row.edge_id,
                    "from_node": row.from_node_name,
                    "to_node": row.to_node_name,
                    "edge_type": row.edge_type,
                    "thermal_rating_mva": float(row.thermal_rating_mva) if row.thermal_rating_mva else None,
                    "downstream_customers": downstream_customers,
                    "criticality_score": criticality_score
                })
        
        # Sort by criticality score
        critical_paths.sort(key=lambda x: x["criticality_score"], reverse=True)
        
        return critical_paths[:20]  # Return top 20
    
    def _get_downstream_assets(
        self,
        node_id: UUID,
        visited: Optional[Set[UUID]] = None
    ) -> Set[UUID]:
        """
        Recursively get all assets downstream of a node.
        """
        if visited is None:
            visited = set()
        
        if node_id in visited:
            return set()
        
        visited.add(node_id)
        downstream_assets = set()
        
        # Find edges from this node
        edges = self.db.query(models.NetworkEdge).filter(
            models.NetworkEdge.from_node_id == node_id
        ).all()
        
        for edge in edges:
            # Get asset at destination node
            dest_node = self.db.query(models.NetworkNode).filter(
                models.NetworkNode.id == edge.to_node_id
            ).first()
            
            if dest_node and dest_node.asset_id:
                downstream_assets.add(dest_node.asset_id)
            
            # Recursively get downstream assets
            downstream_assets.update(
                self._get_downstream_assets(edge.to_node_id, visited)
            )
        
        return downstream_assets
    
    def _count_customers_in_subgraph(
        self,
        node_ids: Set[UUID]
    ) -> Dict[str, Any]:
        """
        Count total customers and load in a subgraph.
        """
        total_customers = 0
        total_load_mw = 0.0
        
        for node_id in node_ids:
            node = self.db.query(models.NetworkNode).filter(
                models.NetworkNode.id == node_id
            ).first()
            
            if node and node.asset_id:
                conn = self.db.query(models.CustomerConnection).filter(
                    models.CustomerConnection.asset_id == node.asset_id
                ).first()
                
                if conn:
                    total_customers += conn.customers_served or 0
                    total_load_mw += float(conn.peak_load_mw or 0)
        
        return {
            "customers": total_customers,
            "load_mw": total_load_mw
        }
