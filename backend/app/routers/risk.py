"""
Risk Calculation API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app import models, schemas
from app.services.risk_calculator import RiskCalculator

router = APIRouter()


@router.get("/summary", response_model=List[schemas.RiskSummary])
def get_risk_summary(
    db: Session = Depends(get_db)
):
    """Get risk summary for all assets."""
    result = db.execute(text("SELECT * FROM risk_summary"))
    return [dict(row._mapping) for row in result]


@router.get("/calculations", response_model=List[schemas.RiskCalculationResponse])
def get_risk_calculations(
    asset_id: Optional[UUID] = None,
    scenario_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all risk calculations, optionally filtered."""
    query = db.query(models.RiskCalculation)
    if asset_id:
        query = query.filter(models.RiskCalculation.asset_id == asset_id)
    if scenario_type:
        query = query.filter(models.RiskCalculation.scenario_type == scenario_type.upper())
    return query.order_by(models.RiskCalculation.calculation_date.desc()).all()


@router.get("/calculations/{calculation_id}", response_model=schemas.RiskCalculationResponse)
def get_risk_calculation(
    calculation_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific risk calculation."""
    calculation = db.query(models.RiskCalculation).filter(
        models.RiskCalculation.id == calculation_id
    ).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Risk calculation not found")
    return calculation


@router.post("/calculate", response_model=schemas.RiskCalculationResult)
def calculate_risk(
    request: schemas.RiskCalculationRequest,
    db: Session = Depends(get_db)
):
    """
    Calculate risk for a specific asset.
    
    Uses physics-based degradation models (Weibull, Arrhenius) to calculate:
    - Annual failure probability
    - Expected annual cost
    - Risk-adjusted NPV
    """
    calculator = RiskCalculator(db)
    return calculator.calculate_asset_risk(
        asset_id=request.asset_id,
        scenario_type=request.scenario_type,
        time_horizon_years=request.time_horizon_years,
        include_confidence_interval=request.include_confidence_interval
    )


@router.post("/calculate-all")
def calculate_risk_for_all_assets(
    scenario_type: str = "BASE_CASE",
    time_horizon_years: int = 10,
    db: Session = Depends(get_db)
):
    """Calculate risk for all active assets."""
    calculator = RiskCalculator(db)
    results = calculator.calculate_all_assets_risk(
        scenario_type=scenario_type,
        time_horizon_years=time_horizon_years
    )
    return {
        "total_assets": len(results),
        "scenario_type": scenario_type,
        "time_horizon_years": time_horizon_years,
        "total_annual_risk": sum(r.expected_annual_cost for r in results),
        "results": results
    }


# ============================================================================
# Consequence Profile Endpoints
# ============================================================================

@router.get("/consequence-profiles", response_model=List[schemas.ConsequenceProfileResponse])
def get_consequence_profiles(
    asset_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    """Get all consequence profiles, optionally filtered by asset."""
    query = db.query(models.ConsequenceProfile)
    if asset_id:
        query = query.filter(models.ConsequenceProfile.asset_id == asset_id)
    return query.order_by(models.ConsequenceProfile.calculation_date.desc()).all()


@router.post("/consequence-profiles", response_model=schemas.ConsequenceProfileResponse, status_code=201)
def create_consequence_profile(
    profile: schemas.ConsequenceProfileCreate,
    db: Session = Depends(get_db)
):
    """Create a new consequence profile."""
    db_profile = models.ConsequenceProfile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.post("/calculate-consequence/{asset_id}")
def calculate_consequence(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Calculate monetized consequence for an asset."""
    calculator = RiskCalculator(db)
    return calculator.calculate_consequence(asset_id)


# ============================================================================
# Customer Connection Endpoints
# ============================================================================

@router.get("/customer-connections", response_model=List[schemas.CustomerConnectionResponse])
def get_customer_connections(
    asset_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    """Get all customer connections, optionally filtered by asset."""
    query = db.query(models.CustomerConnection)
    if asset_id:
        query = query.filter(models.CustomerConnection.asset_id == asset_id)
    return query.all()


@router.post("/customer-connections", response_model=schemas.CustomerConnectionResponse, status_code=201)
def create_customer_connection(
    connection: schemas.CustomerConnectionCreate,
    db: Session = Depends(get_db)
):
    """Create a new customer connection record."""
    db_connection = models.CustomerConnection(**connection.model_dump())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


@router.get("/top-risk-assets")
def get_top_risk_assets(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get top risk assets by annual risk exposure."""
    calculator = RiskCalculator(db)
    return calculator.get_top_risk_assets(limit=limit)


@router.get("/risk-trends/{asset_id}")
def get_risk_trends(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Get risk calculation history for an asset."""
    calculations = db.query(models.RiskCalculation).filter(
        models.RiskCalculation.asset_id == asset_id
    ).order_by(models.RiskCalculation.calculation_date).all()
    
    return {
        "asset_id": asset_id,
        "data_points": len(calculations),
        "trends": [
            {
                "date": c.calculation_date,
                "annual_failure_probability": c.annual_failure_probability,
                "expected_annual_cost": c.expected_annual_cost,
                "scenario_type": c.scenario_type
            }
            for c in calculations
        ]
    }
