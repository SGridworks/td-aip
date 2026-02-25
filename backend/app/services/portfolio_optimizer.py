"""
Portfolio Optimization Service

Implements optimization algorithms for selecting the best investment portfolio
under budget and risk constraints.
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal
import time

from app import models, schemas


class PortfolioOptimizer:
    """Service for optimizing investment portfolios."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def optimize(
        self,
        request: schemas.PortfolioOptimizationRequest
    ) -> schemas.PortfolioOptimizationResult:
        """
        Run portfolio optimization based on the specified method.
        """
        start_time = time.time()
        
        # Get available projects
        projects = self._get_available_projects(
            request.budget_year if hasattr(request, 'budget_year') else 2025,
            request.excluded_projects
        )
        
        if request.optimization_method == "KNAPSACK_GREEDY":
            selected_projects = self._knapsack_greedy(
                projects,
                request.budget_constraint,
                request.mandatory_projects
            )
        elif request.optimization_method == "MILP":
            selected_projects = self._milp_optimize(
                projects,
                request.budget_constraint,
                request.mandatory_projects,
                request.constraints
            )
        else:
            # Default to greedy
            selected_projects = self._knapsack_greedy(
                projects,
                request.budget_constraint,
                request.mandatory_projects
            )
        
        # Calculate portfolio metrics
        total_investment = sum(p.total_budget for p in selected_projects)
        total_risk_reduction = sum(p.risk_reduction_total or 0 for p in selected_projects)
        
        expected_roi = (
            total_risk_reduction / total_investment if total_investment > 0 else 0
        )
        
        # Risk-adjusted return (simplified)
        risk_adjusted_return = expected_roi * 0.85  # Conservative adjustment
        
        # Create scenario record
        scenario = models.PortfolioScenario(
            scenario_name=request.scenario_name,
            budget_constraint=request.budget_constraint,
            risk_tolerance=request.risk_tolerance,
            time_horizon_years=request.time_horizon_years,
            selected_projects=[p.id for p in selected_projects],
            total_investment=Decimal(str(total_investment)),
            total_risk_reduction=Decimal(str(total_risk_reduction)),
            expected_roi=Decimal(str(expected_roi)),
            risk_adjusted_return=Decimal(str(risk_adjusted_return)),
            optimization_date=date.today(),
            optimization_method=request.optimization_method,
            constraints=request.constraints
        )
        self.db.add(scenario)
        self.db.commit()
        self.db.refresh(scenario)
        
        execution_time = time.time() - start_time
        
        return schemas.PortfolioOptimizationResult(
            scenario_id=scenario.id,
            scenario_name=request.scenario_name,
            selected_projects=[p.id for p in selected_projects],
            total_investment=Decimal(str(total_investment)),
            total_risk_reduction=Decimal(str(total_risk_reduction)),
            expected_roi=Decimal(str(expected_roi)),
            risk_adjusted_return=Decimal(str(risk_adjusted_return)),
            budget_utilization_percent=Decimal(str(
                (total_investment / float(request.budget_constraint)) * 100
                if request.budget_constraint > 0 else 0
            )),
            optimization_method=request.optimization_method,
            execution_time_seconds=execution_time
        )
    
    def _get_available_projects(
        self,
        budget_year: int,
        excluded_projects: Optional[List[UUID]] = None
    ) -> List[models.InvestmentProject]:
        """Get available projects for optimization."""
        query = self.db.query(models.InvestmentProject).filter(
            models.InvestmentProject.budget_year == budget_year,
            models.InvestmentProject.status.in_(["PLANNED", "APPROVED"])
        )
        
        if excluded_projects:
            query = query.filter(
                ~models.InvestmentProject.id.in_(excluded_projects)
            )
        
        return query.all()
    
    def _knapsack_greedy(
        self,
        projects: List[models.InvestmentProject],
        budget_constraint: Decimal,
        mandatory_projects: Optional[List[UUID]] = None
    ) -> List[models.InvestmentProject]:
        """
        Greedy knapsack algorithm for portfolio selection.
        
        Selects projects by benefit/cost ratio until budget is exhausted.
        """
        selected = []
        remaining_budget = float(budget_constraint)
        
        # First, add mandatory projects
        if mandatory_projects:
            for project in projects:
                if project.id in mandatory_projects:
                    if remaining_budget >= float(project.total_budget):
                        selected.append(project)
                        remaining_budget -= float(project.total_budget)
        
        # Calculate benefit/cost ratio for remaining projects
        project_scores = []
        for project in projects:
            if project in selected:
                continue
            
            cost = float(project.total_budget)
            benefit = float(project.risk_reduction_total or 0)
            
            if cost > 0:
                score = benefit / cost
                project_scores.append((project, score, cost))
        
        # Sort by benefit/cost ratio (descending)
        project_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Greedily select projects
        for project, score, cost in project_scores:
            if cost <= remaining_budget:
                selected.append(project)
                remaining_budget -= cost
        
        return selected
    
    def _milp_optimize(
        self,
        projects: List[models.InvestmentProject],
        budget_constraint: Decimal,
        mandatory_projects: Optional[List[UUID]] = None,
        constraints: Optional[Dict[str, Any]] = None
    ) -> List[models.InvestmentProject]:
        """
        Mixed Integer Linear Programming optimization.
        
        This is a simplified implementation. In production, you would use
        a proper MILP solver like PuLP, Gurobi, or CPLEX.
        """
        # For now, fall back to greedy with some additional constraints
        selected = self._knapsack_greedy(projects, budget_constraint, mandatory_projects)
        
        # Apply additional constraints if specified
        if constraints:
            # Min risk reduction constraint
            min_risk_reduction = constraints.get("min_risk_reduction")
            if min_risk_reduction:
                total_risk_reduction = sum(
                    p.risk_reduction_total or 0 for p in selected
                )
                
                # If constraint not met, try to add more projects
                if total_risk_reduction < min_risk_reduction:
                    remaining = [p for p in projects if p not in selected]
                    remaining_budget = float(budget_constraint) - sum(
                        p.total_budget for p in selected
                    )
                    
                    # Sort remaining by risk reduction
                    remaining.sort(
                        key=lambda p: p.risk_reduction_total or 0,
                        reverse=True
                    )
                    
                    for project in remaining:
                        if float(project.total_budget) <= remaining_budget:
                            selected.append(project)
                            remaining_budget -= float(project.total_budget)
                            
                            total_risk_reduction += project.risk_reduction_total or 0
                            if total_risk_reduction >= min_risk_reduction:
                                break
        
        return selected
    
    def calculate_intervention_priority(
        self,
        intervention: models.InterventionOption
    ) -> float:
        """
        Calculate priority score for an intervention option.
        
        Considers:
        - Risk reduction per dollar
        - Life extension value
        - Asset criticality
        """
        # Get asset details
        asset = self.db.query(models.Asset).filter(
            models.Asset.id == intervention.asset_id
        ).first()
        
        if not asset:
            return 0.0
        
        # Base score from risk reduction
        risk_reduction = intervention.risk_reduction_percent or 0
        cost = float(intervention.cost_estimate or 1)
        
        risk_score = risk_reduction / cost * 1000  # Normalize
        
        # Criticality multiplier
        criticality_multiplier = asset.criticality or 3
        
        # Life extension value
        life_extension = intervention.life_extension_years or 0
        life_score = life_extension / 10.0  # Normalize to 0-1
        
        # Combined priority score
        priority = (risk_score * criticality_multiplier + life_score) / 10.0
        
        return min(priority, 10.0)  # Cap at 10
    
    def generate_intervention_options(
        self,
        asset_id: UUID
    ) -> List[Dict[str, Any]]:
        """
        Generate intervention options for an asset based on its condition.
        """
        asset = self.db.query(models.Asset).filter(
            models.Asset.id == asset_id
        ).first()
        
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Get current risk
        risk = self.db.query(models.RiskCalculation).filter(
            models.RiskCalculation.asset_id == asset_id,
            models.RiskCalculation.scenario_type == "BASE_CASE"
        ).order_by(models.RiskCalculation.calculation_date.desc()).first()
        
        current_pof = float(risk.annual_failure_probability) if risk else 0.05
        current_risk = float(risk.expected_annual_cost) if risk else 50000
        
        # Get asset type for replacement cost
        asset_type = self.db.query(models.AssetType).filter(
            models.AssetType.id == asset.asset_type_id
        ).first()
        
        options = []
        
        # Option 1: Replace
        replacement_cost = self._estimate_replacement_cost(asset)
        options.append({
            "intervention_type": "REPLACE",
            "description": f"Replace {asset.name} with new equipment",
            "cost_estimate": replacement_cost,
            "risk_reduction_percent": 95.0,
            "failure_probability_reduction": current_pof * 0.95,
            "life_extension_years": asset_type.typical_lifespan_years if asset_type else 30,
            "benefit_cost_ratio": (current_risk * 10) / replacement_cost if replacement_cost > 0 else 0
        })
        
        # Option 2: Major refurbishment (for transformers)
        if asset_type and asset_type.category == "TRANSFORMER":
            refurb_cost = replacement_cost * 0.4
            options.append({
                "intervention_type": "REFURBISH_MAJOR",
                "description": "Major refurbishment: rewind, new bushings, OLTC rebuild",
                "cost_estimate": refurb_cost,
                "risk_reduction_percent": 70.0,
                "failure_probability_reduction": current_pof * 0.70,
                "life_extension_years": 15,
                "benefit_cost_ratio": (current_risk * 7) / refurb_cost if refurb_cost > 0 else 0
            })
        
        # Option 3: Enhanced monitoring
        monitor_cost = replacement_cost * 0.08
        options.append({
            "intervention_type": "MONITOR_ENHANCE",
            "description": "Install online monitoring and predictive analytics",
            "cost_estimate": monitor_cost,
            "risk_reduction_percent": 25.0,
            "failure_probability_reduction": current_pof * 0.25,
            "life_extension_years": 0,
            "benefit_cost_ratio": (current_risk * 2.5) / monitor_cost if monitor_cost > 0 else 0
        })
        
        # Option 4: Maintain (baseline)
        options.append({
            "intervention_type": "MAINTAIN_PREVENTIVE",
            "description": "Continue preventive maintenance program",
            "cost_estimate": replacement_cost * 0.03,
            "risk_reduction_percent": 10.0,
            "failure_probability_reduction": current_pof * 0.10,
            "life_extension_years": 3,
            "benefit_cost_ratio": 1.0
        })
        
        return options
    
    def _estimate_replacement_cost(self, asset: models.Asset) -> float:
        """Estimate replacement cost for an asset."""
        # Get failure modes for cost reference
        failure_modes = self.db.query(models.FailureMode).filter(
            models.FailureMode.asset_type_id == asset.asset_type_id
        ).all()
        
        if failure_modes:
            avg_cost = sum(
                float(fm.replacement_cost_avg or 0) for fm in failure_modes
            ) / len(failure_modes)
            return avg_cost
        
        # Default estimates by category
        defaults = {
            "TRANSFORMER": 800000,
            "BREAKER": 400000,
            "LINE": 200000,
            "SWITCH": 50000,
            "REGULATOR": 150000,
            "CAPACITOR": 75000,
            "RECLOSER": 50000,
            "SECTIONALIZER": 30000
        }
        
        asset_type = self.db.query(models.AssetType).filter(
            models.AssetType.id == asset.asset_type_id
        ).first()
        
        return defaults.get(asset_type.category if asset_type else "", 100000)
