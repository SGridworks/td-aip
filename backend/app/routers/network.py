"""
Network Analysis API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app import models, schemas
from app.services.network_analyzer import NetworkAnalyzer

router = APIRouter()


@router.get("/nodes", response_model=List[schemas.NetworkNodeResponse])
def get_network_nodes(
    node_type: Optional[str] = None,
    voltage_level: Optional[str] = None,
    operational_state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all network nodes, optionally filtered."""
    query = db.query(models.NetworkNode)
    if node_type:
        query = query.filter(models.NetworkNode.node_type == node_type.upper())
    if voltage_level:
        query = query.filter(models.NetworkNode.voltage_level == voltage_level)
    if operational_state:
        query = query.filter(models.NetworkNode.operational_state == operational_state.upper())
    return query.all()


@router.post("/nodes", response_model=schemas.NetworkNodeResponse, status_code=201)
def create_network_node(
    node: schemas.NetworkNodeCreate,
    db: Session = Depends(get_db)
):
    """Create a new network node."""
    db_node = models.NetworkNode(**node.model_dump())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node


@router.get("/edges", response_model=List[schemas.NetworkEdgeResponse])
def get_network_edges(
    edge_type: Optional[str] = None,
    from_node_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    """Get all network edges, optionally filtered."""
    query = db.query(models.NetworkEdge)
    if edge_type:
        query = query.filter(models.NetworkEdge.edge_type == edge_type.upper())
    if from_node_id:
        query = query.filter(models.NetworkEdge.from_node_id == from_node_id)
    return query.all()


@router.post("/edges", response_model=schemas.NetworkEdgeResponse, status_code=201)
def create_network_edge(
    edge: schemas.NetworkEdgeCreate,
    db: Session = Depends(get_db)
):
    """Create a new network edge."""
    db_edge = models.NetworkEdge(**edge.model_dump())
    db.add(db_edge)
    db.commit()
    db.refresh(db_edge)
    return db_edge


@router.get("/connectivity", response_model=List[schemas.NetworkConnectivity])
def get_network_connectivity(
    db: Session = Depends(get_db)
):
    """Get network connectivity view."""
    result = db.execute(text("SELECT * FROM network_connectivity"))
    return [dict(row._mapping) for row in result]


@router.get("/switching-paths", response_model=List[schemas.SwitchingPathResponse])
def get_switching_paths(
    source_node_id: Optional[UUID] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all switching paths, optionally filtered."""
    query = db.query(models.SwitchingPath)
    if source_node_id:
        query = query.filter(models.SwitchingPath.source_node_id == source_node_id)
    if is_active is not None:
        query = query.filter(models.SwitchingPath.is_active == is_active)
    return query.all()


@router.post("/switching-paths", response_model=schemas.SwitchingPathResponse, status_code=201)
def create_switching_path(
    path: schemas.SwitchingPathCreate,
    db: Session = Depends(get_db)
):
    """Create a new switching path."""
    db_path = models.SwitchingPath(**path.model_dump())
    db.add(db_path)
    db.commit()
    db.refresh(db_path)
    return db_path


@router.post("/analyze", response_model=schemas.NetworkAnalysisResponse)
def analyze_network(
    request: schemas.NetworkAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Perform network analysis for a given node.
    
    Analysis types:
    - connectivity: Find all connected nodes
    - switching_paths: Find alternative feed paths
    - load_flow: Analyze load flow and identify at-risk customers
    """
    analyzer = NetworkAnalyzer(db)
    
    if request.analysis_type == "connectivity":
        return analyzer.analyze_connectivity(request.node_id, request.max_depth)
    elif request.analysis_type == "switching_paths":
        return analyzer.analyze_switching_paths(request.node_id)
    elif request.analysis_type == "load_flow":
        return analyzer.analyze_load_flow(request.node_id)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown analysis type: {request.analysis_type}")


@router.get("/asset/{asset_id}/downstream-customers")
def get_downstream_customers(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all customers downstream of a given asset."""
    analyzer = NetworkAnalyzer(db)
    return analyzer.get_downstream_customers(asset_id)


@router.get("/critical-paths")
def get_critical_paths(
    db: Session = Depends(get_db)
):
    """Identify critical paths in the network based on customer impact."""
    analyzer = NetworkAnalyzer(db)
    return analyzer.identify_critical_paths()
