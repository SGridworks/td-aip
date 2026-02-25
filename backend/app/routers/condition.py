"""
Condition Assessment API Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/assessments", response_model=List[schemas.ConditionAssessmentResponse])
def get_condition_assessments(
    asset_id: Optional[UUID] = None,
    assessment_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all condition assessments, optionally filtered."""
    query = db.query(models.ConditionAssessment)
    if asset_id:
        query = query.filter(models.ConditionAssessment.asset_id == asset_id)
    if assessment_type:
        query = query.filter(models.ConditionAssessment.assessment_type == assessment_type.upper())
    return query.order_by(models.ConditionAssessment.assessment_date.desc()).all()


@router.get("/assessments/{assessment_id}", response_model=schemas.ConditionAssessmentResponse)
def get_condition_assessment(
    assessment_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific condition assessment."""
    assessment = db.query(models.ConditionAssessment).filter(
        models.ConditionAssessment.id == assessment_id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Condition assessment not found")
    return assessment


@router.post("/assessments", response_model=schemas.ConditionAssessmentResponse, status_code=201)
def create_condition_assessment(
    assessment: schemas.ConditionAssessmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new condition assessment."""
    # Verify asset exists
    asset = db.query(models.Asset).filter(models.Asset.id == assessment.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db_assessment = models.ConditionAssessment(**assessment.model_dump())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.get("/asset/{asset_id}/latest", response_model=Optional[schemas.ConditionAssessmentResponse])
def get_latest_condition_assessment(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Get the latest condition assessment for an asset."""
    assessment = db.query(models.ConditionAssessment).filter(
        models.ConditionAssessment.asset_id == asset_id
    ).order_by(models.ConditionAssessment.assessment_date.desc()).first()
    return assessment


# ============================================================================
# Diagnostic Test Endpoints
# ============================================================================

@router.get("/diagnostic-tests", response_model=List[schemas.DiagnosticTestResponse])
def get_diagnostic_tests(
    asset_id: Optional[UUID] = None,
    test_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all diagnostic tests, optionally filtered."""
    query = db.query(models.DiagnosticTest)
    if asset_id:
        query = query.filter(models.DiagnosticTest.asset_id == asset_id)
    if test_type:
        query = query.filter(models.DiagnosticTest.test_type == test_type.upper())
    return query.order_by(models.DiagnosticTest.test_date.desc()).all()


@router.post("/diagnostic-tests", response_model=schemas.DiagnosticTestResponse, status_code=201)
def create_diagnostic_test(
    test: schemas.DiagnosticTestCreate,
    db: Session = Depends(get_db)
):
    """Create a new diagnostic test record."""
    db_test = models.DiagnosticTest(**test.model_dump())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


@router.get("/asset/{asset_id}/dga-latest")
def get_latest_dga(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Get the latest DGA (Dissolved Gas Analysis) for an asset."""
    test = db.query(models.DiagnosticTest).filter(
        models.DiagnosticTest.asset_id == asset_id,
        models.DiagnosticTest.test_type == "DGA"
    ).order_by(models.DiagnosticTest.test_date.desc()).first()
    
    if not test:
        raise HTTPException(status_code=404, detail="No DGA data found for this asset")
    
    return {
        "asset_id": asset_id,
        "test_date": test.test_date,
        "dissolved_gases": test.dissolved_gases,
        "key_gas": test.dga_key_gas,
        "rogers_ratio": test.dga_rogers_ratio,
        "result": test.overall_test_result
    }


# ============================================================================
# Monitoring Data Endpoints
# ============================================================================

@router.get("/monitoring-data", response_model=List[schemas.MonitoringDataResponse])
def get_monitoring_data(
    asset_id: Optional[UUID] = None,
    sensor_type: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get monitoring data, optionally filtered."""
    query = db.query(models.MonitoringData)
    if asset_id:
        query = query.filter(models.MonitoringData.asset_id == asset_id)
    if sensor_type:
        query = query.filter(models.MonitoringData.sensor_type == sensor_type.upper())
    return query.order_by(models.MonitoringData.timestamp.desc()).limit(limit).all()


@router.post("/monitoring-data", response_model=schemas.MonitoringDataResponse, status_code=201)
def create_monitoring_data(
    data: schemas.MonitoringDataCreate,
    db: Session = Depends(get_db)
):
    """Create a new monitoring data record."""
    db_data = models.MonitoringData(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


@router.get("/asset/{asset_id}/health-trend")
def get_health_trend(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Get health score trend for an asset from condition assessments."""
    assessments = db.query(models.ConditionAssessment).filter(
        models.ConditionAssessment.asset_id == asset_id
    ).order_by(models.ConditionAssessment.assessment_date).all()
    
    return {
        "asset_id": asset_id,
        "data_points": len(assessments),
        "trend": [
            {
                "date": a.assessment_date,
                "health_index": a.health_index,
                "overall_condition": a.overall_condition,
                "probability_of_failure": a.probability_of_failure,
                "remaining_life_years": a.remaining_life_years
            }
            for a in assessments
        ]
    }
