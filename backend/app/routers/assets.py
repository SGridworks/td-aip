"""
Asset API Router
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/types", response_model=List[schemas.AssetTypeResponse])
def get_asset_types(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all asset types, optionally filtered by category."""
    query = db.query(models.AssetType)
    if category:
        query = query.filter(models.AssetType.category == category.upper())
    return query.all()


@router.post("/types", response_model=schemas.AssetTypeResponse, status_code=201)
def create_asset_type(
    asset_type: schemas.AssetTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new asset type."""
    db_asset_type = models.AssetType(**asset_type.model_dump())
    db.add(db_asset_type)
    db.commit()
    db.refresh(db_asset_type)
    return db_asset_type


@router.get("/locations", response_model=List[schemas.AssetLocationResponse])
def get_asset_locations(
    service_territory: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all asset locations, optionally filtered by service territory."""
    query = db.query(models.AssetLocation)
    if service_territory:
        query = query.filter(models.AssetLocation.service_territory == service_territory)
    return query.all()


@router.post("/locations", response_model=schemas.AssetLocationResponse, status_code=201)
def create_asset_location(
    location: schemas.AssetLocationCreate,
    db: Session = Depends(get_db)
):
    """Create a new asset location."""
    db_location = models.AssetLocation(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


@router.get("", response_model=List[schemas.AssetResponse])
def get_assets(
    asset_type_id: Optional[UUID] = None,
    location_id: Optional[UUID] = None,
    status: Optional[str] = None,
    criticality: Optional[int] = None,
    min_health_score: Optional[float] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all assets with optional filtering."""
    query = db.query(models.Asset)
    
    if asset_type_id:
        query = query.filter(models.Asset.asset_type_id == asset_type_id)
    if location_id:
        query = query.filter(models.Asset.location_id == location_id)
    if status:
        query = query.filter(models.Asset.status == status.upper())
    if criticality:
        query = query.filter(models.Asset.criticality == criticality)
    if min_health_score is not None:
        query = query.filter(models.Asset.health_score >= min_health_score)
    
    return query.offset(skip).limit(limit).all()


@router.get("/summary", response_model=List[schemas.AssetHealthSummary])
def get_asset_health_summary(
    db: Session = Depends(get_db)
):
    """Get asset health summary for all assets."""
    # This uses the database view
    from sqlalchemy import text
    result = db.execute(text("SELECT * FROM asset_health_summary"))
    return [dict(row._mapping) for row in result]


@router.get("/{asset_id}", response_model=schemas.AssetResponse)
def get_asset(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific asset by ID."""
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("", response_model=schemas.AssetResponse, status_code=201)
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db)
):
    """Create a new asset."""
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.put("/{asset_id}", response_model=schemas.AssetResponse)
def update_asset(
    asset_id: UUID,
    asset_update: schemas.AssetUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing asset."""
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    update_data = asset_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.delete("/{asset_id}", status_code=204)
def delete_asset(
    asset_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete an asset."""
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db.delete(db_asset)
    db.commit()
    return None


# ============================================================================
# Failure Mode Endpoints
# ============================================================================

@router.get("/failure-modes", response_model=List[schemas.FailureModeResponse])
def get_failure_modes(
    asset_type_id: Optional[UUID] = None,
    failure_category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all failure modes, optionally filtered."""
    query = db.query(models.FailureMode)
    if asset_type_id:
        query = query.filter(models.FailureMode.asset_type_id == asset_type_id)
    if failure_category:
        query = query.filter(models.FailureMode.failure_category == failure_category.upper())
    return query.all()


@router.post("/failure-modes", response_model=schemas.FailureModeResponse, status_code=201)
def create_failure_mode(
    failure_mode: schemas.FailureModeCreate,
    db: Session = Depends(get_db)
):
    """Create a new failure mode."""
    db_failure_mode = models.FailureMode(**failure_mode.model_dump())
    db.add(db_failure_mode)
    db.commit()
    db.refresh(db_failure_mode)
    return db_failure_mode


# ============================================================================
# Degradation Model Endpoints
# ============================================================================

@router.get("/degradation-models", response_model=List[schemas.DegradationModelResponse])
def get_degradation_models(
    failure_mode_id: Optional[UUID] = None,
    model_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all degradation models, optionally filtered."""
    query = db.query(models.DegradationModel)
    if failure_mode_id:
        query = query.filter(models.DegradationModel.failure_mode_id == failure_mode_id)
    if model_type:
        query = query.filter(models.DegradationModel.model_type == model_type.upper())
    return query.all()


@router.post("/degradation-models", response_model=schemas.DegradationModelResponse, status_code=201)
def create_degradation_model(
    degradation_model: schemas.DegradationModelCreate,
    db: Session = Depends(get_db)
):
    """Create a new degradation model."""
    db_model = models.DegradationModel(**degradation_model.model_dump())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model
