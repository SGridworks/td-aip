# AIP Core - FastAPI Backend

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session management
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── assets.py        # Asset-related models
│   │   ├── network.py       # Network topology models
│   │   ├── failure_modes.py # Failure mode and degradation models
│   │   ├── condition.py     # Condition assessment models
│   │   ├── risk.py          # Risk calculation models
│   │   └── investment.py    # Investment and portfolio models
│   ├── schemas/             # Pydantic schemas for API
│   │   ├── __init__.py
│   │   ├── assets.py
│   │   ├── network.py
│   │   ├── risk.py
│   │   └── investment.py
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── assets.py        # Asset endpoints
│   │   ├── network.py       # Network analysis endpoints
│   │   ├── risk.py          # Risk calculation endpoints
│   │   ├── condition.py     # Condition assessment endpoints
│   │   └── investment.py    # Investment/portfolio endpoints
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── risk_calculator.py    # Risk calculation engine
│   │   ├── network_analyzer.py   # Network connectivity analysis
│   │   ├── degradation_models.py # Physics-based degradation
│   │   └── portfolio_optimizer.py # Portfolio optimization
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── tests/                   # Test suite
├── alembic/                 # Database migrations
├── requirements.txt
├── Dockerfile
└── README.md
```

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

## API Documentation

Once running, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Features

1. **Asset Management**: Full CRUD for T&D assets with T&D-specific taxonomy
2. **Risk Calculation**: Physics-based degradation models (Weibull, Arrhenius)
3. **Network Analysis**: Connectivity and switching path analysis
4. **Monetized Risk**: Risk in dollars, not scores
5. **Portfolio Optimization**: Investment portfolio optimization under constraints
