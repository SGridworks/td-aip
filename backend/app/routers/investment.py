"""
Investment and Portfolio API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app import models, schemas
from app.services.portfolio_optimizer import PortfolioOptimizer

router = APIRouter()


# ============================================================================
# Intervention Options Endpoints
# ============================================================================

@router.get("/interventions", response_model=List[schemas.InterventionOptionResponse])
def get_intervention_options(
    asset_id: Optional[UUID] = None,
    status: Optional[str] = None,
    min_priority: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Get all intervention options, optionally filtered."""
    query = db.query(models.InterventionOption)
    if asset_id:
        query = query.filter(models.InterventionOption.asset_id == asset_id)
    if status:
        query = query.filter(models.InterventionOption.status == status.upper())
    if min_priority:
        query = query.filter(models.InterventionOption.priority_score >= min_priority)
    return query.order_by(models.InterventionOption.priority_score.desc()).all()


@router.get("/interventions/{intervention_id}", response_model=schemas.InterventionOptionResponse)
def get_intervention_option(
    intervention_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific intervention option."""
    intervention = db.query(models.InterventionOption).filter(
        models.InterventionOption.id == intervention_id
    ).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention option not found")
    return intervention


@router.post("/interventions", response_model=schemas.InterventionOptionResponse, status_code=201)
def create_intervention_option(
    intervention: schemas.InterventionOptionCreate,
    db: Session = Depends(get_db)
):
    """Create a new intervention option."""
    db_intervention = models.InterventionOption(**intervention.model_dump())
    db.add(db_intervention)
    db.commit()
    db.refresh(db_intervention)
    return db_intervention


@router.put("/interventions/{intervention_id}", response_model=schemas.InterventionOptionResponse)
def update_intervention_option(
    intervention_id: UUID,
    status: str,
    db: Session = Depends(get_db)
):
    """Update intervention option status."""
    intervention = db.query(models.InterventionOption).filter(
        models.InterventionOption.id == intervention_id
    ).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention option not found")
    
    intervention.status = status.upper()
    db.commit()
    db.refresh(intervention)
    return intervention


@router.get("/interventions/by-asset/{asset_id}")
def get_interventions_by_asset(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all intervention options for a specific asset with risk context."""
    interventions = db.query(models.InterventionOption).filter(
        models.InterventionOption.asset_id == asset_id
    ).order_by(models.InterventionOption.priority_score.desc()).all()
    
    # Get current risk for context
    risk = db.query(models.RiskCalculation).filter(
        models.RiskCalculation.asset_id == asset_id,
        models.RiskCalculation.scenario_type == "BASE_CASE"
    ).order_by(models.RiskCalculation.calculation_date.desc()).first()
    
    return {
        "asset_id": asset_id,
        "current_annual_risk": risk.expected_annual_cost if risk else None,
        "current_pof": risk.annual_failure_probability if risk else None,
        "interventions": interventions
    }


# ============================================================================
# Investment Project Endpoints
# ============================================================================

@router.get("/projects", response_model=List[schemas.InvestmentProjectResponse])
def get_investment_projects(
    budget_year: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all investment projects, optionally filtered."""
    query = db.query(models.InvestmentProject)
    if budget_year:
        query = query.filter(models.InvestmentProject.budget_year == budget_year)
    if status:
        query = query.filter(models.InvestmentProject.status == status.upper())
    return query.order_by(models.InvestmentProject.priority_rank).all()


@router.get("/projects/{project_id}", response_model=schemas.InvestmentProjectResponse)
def get_investment_project(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific investment project."""
    project = db.query(models.InvestmentProject).filter(
        models.InvestmentProject.id == project_id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Investment project not found")
    return project


@router.post("/projects", response_model=schemas.InvestmentProjectResponse, status_code=201)
def create_investment_project(
    project: schemas.InvestmentProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new investment project."""
    db_project = models.InvestmentProject(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.put("/projects/{project_id}", response_model=schemas.InvestmentProjectResponse)
def update_investment_project(
    project_id: UUID,
    project_update: schemas.InvestmentProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update an investment project."""
    project = db.query(models.InvestmentProject).filter(
        models.InvestmentProject.id == project_id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Investment project not found")
    
    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/summary/{budget_year}")
def get_projects_summary(
    budget_year: int,
    db: Session = Depends(get_db)
):
    """Get summary of projects for a budget year."""
    projects = db.query(models.InvestmentProject).filter(
        models.InvestmentProject.budget_year == budget_year
    ).all()
    
    total_budget = sum(p.total_budget for p in projects)
    total_risk_reduction = sum(p.risk_reduction_total or 0 for p in projects)
    
    return {
        "budget_year": budget_year,
        "total_projects": len(projects),
        "total_budget": total_budget,
        "total_risk_reduction": total_risk_reduction,
        "risk_reduction_per_dollar": total_risk_reduction / total_budget if total_budget > 0 else 0,
        "projects_by_status": {
            status: len([p for p in projects if p.status == status])
            for status in set(p.status for p in projects)
        }
    }


# ============================================================================
# Portfolio Scenario Endpoints
# ============================================================================

@router.get("/scenarios", response_model=List[schemas.PortfolioScenarioResponse])
def get_portfolio_scenarios(
    db: Session = Depends(get_db)
):
    """Get all portfolio scenarios."""
    return db.query(models.PortfolioScenario).order_by(
        models.PortfolioScenario.optimization_date.desc()
    ).all()


@router.get("/scenarios/{scenario_id}", response_model=schemas.PortfolioScenarioResponse)
def get_portfolio_scenario(
    scenario_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific portfolio scenario."""
    scenario = db.query(models.PortfolioScenario).filter(
        models.PortfolioScenario.id == scenario_id
    ).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Portfolio scenario not found")
    return scenario


@router.post("/scenarios", response_model=schemas.PortfolioScenarioResponse, status_code=201)
def create_portfolio_scenario(
    scenario: schemas.PortfolioScenarioCreate,
    db: Session = Depends(get_db)
):
    """Create a new portfolio scenario."""
    db_scenario = models.PortfolioScenario(**scenario.model_dump())
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario


@router.post("/optimize", response_model=schemas.PortfolioOptimizationResult)
def optimize_portfolio(
    request: schemas.PortfolioOptimizationRequest,
    db: Session = Depends(get_db)
):
    """
    Run portfolio optimization to select optimal projects under budget constraints.
    
    Optimization methods:
    - KNAPSACK_GREEDY: Fast greedy algorithm by benefit/cost ratio
    - MILP: Mixed Integer Linear Programming for optimal solution
    """
    optimizer = PortfolioOptimizer(db)
    return optimizer.optimize(request)


@router.get("/scenarios/{scenario_id}/details")
def get_scenario_details(
    scenario_id: UUID,
    db: Session = Depends(get_db)
):
    """Get detailed information about a portfolio scenario including selected projects."""
    scenario = db.query(models.PortfolioScenario).filter(
        models.PortfolioScenario.id == scenario_id
    ).first()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Portfolio scenario not found")
    
    # Get project details
    projects = []
    if scenario.selected_projects:
        for project_id in scenario.selected_projects:
            project = db.query(models.InvestmentProject).filter(
                models.InvestmentProject.id == project_id
            ).first()
            if project:
                projects.append(project)
    
    return {
        "scenario": scenario,
        "selected_projects": projects,
        "project_count": len(projects),
        "budget_utilization": (
            sum(p.total_budget for p in projects) / scenario.budget_constraint * 100
            if scenario.budget_constraint else 0
        )
    }


@router.get("/dashboard")
def get_investment_dashboard(
    budget_year: int = 2025,
    db: Session = Depends(get_db)
):
    """Get investment dashboard summary."""
    # Get project stats
    projects = db.query(models.InvestmentProject).filter(
        models.InvestmentProject.budget_year == budget_year
    ).all()
    
    # Get intervention stats
    interventions = db.query(models.InterventionOption).filter(
        models.InterventionOption.status == "PROPOSED"
    ).all()
    
    # Get risk summary
    from sqlalchemy import text
    risk_result = db.execute(text("""
        SELECT 
            COUNT(*) as asset_count,
            SUM(expected_annual_cost) as total_annual_risk,
            AVG(annual_failure_probability) as avg_pof
        FROM risk_summary
        WHERE expected_annual_cost IS NOT NULL
    """))
    risk_data = risk_result.fetchone()
    
    return {
        "budget_year": budget_year,
        "projects": {
            "total": len(projects),
            "total_budget": sum(p.total_budget for p in projects),
            "total_risk_reduction": sum(p.risk_reduction_total or 0 for p in projects),
            "by_status": {
                status: len([p for p in projects if p.status == status])
                for status in set(p.status for p in projects)
            }
        },
        "interventions": {
            "proposed": len(interventions),
            "total_cost": sum(i.cost_estimate or 0 for i in interventions),
            "total_risk_reduction": sum(
                (i.risk_reduction_percent or 0) * (i.cost_estimate or 0) / 100
                for i in interventions
            )
        },
        "risk_summary": {
            "assets_analyzed": risk_data.asset_count if risk_data else 0,
            "total_annual_risk": float(risk_data.total_annual_risk) if risk_data and risk_data.total_annual_risk else 0,
            "average_failure_probability": float(risk_data.avg_pof) if risk_data and risk_data.avg_pof else 0
        }
    }
