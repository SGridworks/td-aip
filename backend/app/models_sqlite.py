"""
SQLite-compatible SQLAlchemy ORM models for AIP Core (Prototype)
"""

from sqlalchemy import Column, String, DateTime, Date, Numeric, Integer, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class AssetType(Base):
    """T&D-specific asset taxonomy."""
    __tablename__ = "asset_types"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    category = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    voltage_classes = Column(JSON)  # Store as JSON array
    typical_lifespan_years = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    assets = relationship("Asset", back_populates="asset_type")
    failure_modes = relationship("FailureMode", back_populates="asset_type")


class AssetLocation(Base):
    """Geographic and service territory information."""
    __tablename__ = "asset_locations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    substation_id = Column(String(50), nullable=False)
    substation_name = Column(String(200))
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    voltage_level = Column(String(20))
    service_territory = Column(String(100))
    climate_zone = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    assets = relationship("Asset", back_populates="location")


class Asset(Base):
    """Core asset register."""
    __tablename__ = "assets"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    asset_type_id = Column(String(36), ForeignKey("asset_types.id"), nullable=False)
    location_id = Column(String(36), ForeignKey("asset_locations.id"))
    name = Column(String(200), nullable=False)
    manufacturer = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    install_date = Column(Date, nullable=False)
    mva_rating = Column(Numeric(10, 3))
    voltage_primary_kv = Column(Numeric(8, 3))
    voltage_secondary_kv = Column(Numeric(8, 3))
    health_score = Column(Numeric(4, 3))
    criticality = Column(Integer)
    status = Column(String(20), default='IN_SERVICE')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    asset_type = relationship("AssetType", back_populates="assets")
    location = relationship("AssetLocation", back_populates="assets")


class FailureMode(Base):
    """T&D-specific failure mechanisms."""
    __tablename__ = "failure_modes"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    asset_type_id = Column(String(36), ForeignKey("asset_types.id"), nullable=False)
    failure_category = Column(String(50), nullable=False)
    mechanism = Column(String(100), nullable=False)
    description = Column(Text)
    typical_causes = Column(JSON)
    precursors = Column(JSON)
    failure_rate_base = Column(Numeric(10, 6))
    repair_cost_avg = Column(Numeric(12, 2))
    replacement_cost_avg = Column(Numeric(12, 2))
    outage_hours_avg = Column(Numeric(6, 2))
    safety_risk = Column(Integer)
    environmental_risk = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    asset_type = relationship("AssetType", back_populates="failure_modes")


class InvestmentProject(Base):
    """Investment projects for asset intervention."""
    __tablename__ = "investment_projects"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    project_type = Column(String(50), nullable=False)  # replace, refurbish, inspect, maintain
    status = Column(String(20), default='proposed')  # proposed, approved, in_progress, completed
    priority_score = Column(Numeric(5, 2))
    estimated_cost = Column(Numeric(12, 2))
    estimated_benefit = Column(Numeric(12, 2))
    risk_reduction_value = Column(Numeric(12, 2))
    start_date = Column(Date)
    completion_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
