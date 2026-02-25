"""Simple FastAPI for AIP prototype"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import sys

sys.path.insert(0, '.')
from app.database import SessionLocal, engine
from app.models_sqlite import AssetType, AssetLocation, Asset, InvestmentProject

app = FastAPI(title="AIP Prototype API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/v1/assets")
def list_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    return [{"id": a.id, "name": a.name, "manufacturer": a.manufacturer, 
             "model": a.model, "health_score": float(a.health_score) if a.health_score else None,
             "status": a.status, "criticality": a.criticality} for a in assets]

@app.get("/api/v1/assets/{asset_id}")
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    a = db.query(Asset).filter(Asset.id == asset_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"id": a.id, "name": a.name, "manufacturer": a.manufacturer,
            "model": a.model, "health_score": float(a.health_score) if a.health_score else None,
            "status": a.status, "criticality": a.criticality}

@app.get("/api/v1/investment/projects")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(InvestmentProject).all()
    return [{"id": p.id, "name": p.name, "description": p.description,
             "status": p.status, "estimated_cost": float(p.estimated_cost) if p.estimated_cost else None,
             "priority_score": float(p.priority_score) if p.priority_score else None} for p in projects]

@app.get("/health")
def health():
    return {"status": "ok"}
