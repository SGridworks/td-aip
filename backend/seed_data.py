"""Seed script for AIP prototype data"""
import sys
from datetime import date
sys.path.insert(0, '.')

from app.database import engine, Base, SessionLocal
from app.models_sqlite import AssetType, AssetLocation, Asset, FailureMode, InvestmentProject

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(AssetType).first():
        print("Database already seeded")
        db.close()
        return
    
    types = [
        AssetType(category="TRANSFORMER", name="Power Transformer", 
                 description="Oil-immersed power transformer", 
                 voltage_classes=["69kV", "138kV", "230kV"], typical_lifespan_years=40),
        AssetType(category="BREAKER", name="SF6 Circuit Breaker",
                 description="SF6 gas-insulated high voltage circuit breaker",
                 voltage_classes=["69kV", "138kV"], typical_lifespan_years=35),
        AssetType(category="LINE", name="Overhead Transmission Line",
                 description="Overhead conductor transmission line",
                 voltage_classes=["69kV", "138kV"], typical_lifespan_years=50),
    ]
    db.add_all(types)
    db.flush()
    
    locations = [
        AssetLocation(substation_id="SUB-001", substation_name="Northside Substation",
                     latitude=40.7589, longitude=-73.9851, voltage_level="138kV",
                     service_territory="North Metro", climate_zone="Temperate"),
        AssetLocation(substation_id="SUB-002", substation_name="Westside Substation",
                     latitude=40.7505, longitude=-73.9934, voltage_level="138kV",
                     service_territory="West Metro", climate_zone="Temperate"),
    ]
    db.add_all(locations)
    db.flush()
    
    assets = [
        Asset(asset_type_id=types[0].id, location_id=locations[0].id,
              name="TX-N-001", manufacturer="ABB", model="TRE-138-69-60",
              serial_number="SN-1998-001", install_date=date(1998, 3, 15),
              mva_rating=60.0, voltage_primary_kv=138.0, voltage_secondary_kv=69.0,
              health_score=0.72, criticality=5, status="IN_SERVICE"),
        Asset(asset_type_id=types[0].id, location_id=locations[1].id,
              name="TX-W-001", manufacturer="Siemens", model="GST-138-69-75",
              serial_number="SN-2002-045", install_date=date(2002, 7, 22),
              mva_rating=75.0, voltage_primary_kv=138.0, voltage_secondary_kv=69.0,
              health_score=0.85, criticality=5, status="IN_SERVICE"),
    ]
    db.add_all(assets)
    
    projects = [
        InvestmentProject(name="Transformer T1 Replacement", 
                         description="Replace aging transformer TX-N-001",
                         project_type="replace", status="proposed",
                         priority_score=8.5, estimated_cost=2500000,
                         estimated_benefit=4200000, risk_reduction_value=1700000),
    ]
    db.add_all(projects)
    
    db.commit()
    db.close()
    print("Database seeded successfully")

if __name__ == "__main__":
    seed()
