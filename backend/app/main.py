"""
FastAPI application entry point for T&D Asset Investment Planning (AIP) System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.routers import assets, network, risk, condition, investment


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    engine.dispose()


app = FastAPI(
    title="T&D Asset Investment Planning (AIP) API",
    description="""
    Core backend API for T&D-specific Asset Investment Planning.
    
    ## Features
    
    * **Asset Management**: T&D-specific taxonomy (transformers, breakers, lines, switches)
    * **Failure Mode Catalog**: Physics-based degradation models from day one
    * **Network Analysis**: Connectivity and switching path analysis
    * **Risk Calculation**: Monetized risk ($) with Weibull/Arrhenius models
    * **Portfolio Optimization**: Investment portfolio optimization under constraints
    
    ## The 6-Layer Risk Framework
    
    1. **Asset Inventory**: T&D-specific taxonomy, locations, ratings
    2. **Asset Condition**: Physics-based degradation (Weibull, Arrhenius)
    3. **Network Impact**: Connectivity, switching paths, load transfer
    4. **Monetized Consequence**: Customer impact, safety, regulatory costs in $
    5. **Intervention Economics**: Cost-benefit of replacement, refurbishment
    6. **Portfolio Optimization**: Multi-asset decisions under constraints
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(assets.router, prefix="/api/v1/assets", tags=["Assets"])
app.include_router(network.router, prefix="/api/v1/network", tags=["Network"])
app.include_router(risk.router, prefix="/api/v1/risk", tags=["Risk"])
app.include_router(condition.router, prefix="/api/v1/condition", tags=["Condition"])
app.include_router(investment.router, prefix="/api/v1/investment", tags=["Investment"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "T&D Asset Investment Planning (AIP) API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "aip-core-api"}
