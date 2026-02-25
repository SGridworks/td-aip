# T&D Asset Investment Planning (AIP) - Core System

A production-ready backend for T&D-specific Asset Investment Planning with physics-based degradation models, network-aware analysis, and monetized risk calculations.

## Features

### 1. T&D-Specific Taxonomy
- **Transformers**: Power transformers, distribution transformers
- **Circuit Breakers**: SF6 breakers, vacuum breakers
- **Lines**: Overhead transmission, underground distribution cables
- **Switches**: Air-break switches, load break switches
- **Other**: Voltage regulators, capacitor banks, reclosers, sectionalizers

### 2. Failure Mode Catalog (Day One)
Physics-based failure mechanisms:
- **Transformers**: Oil degradation, winding failure, bushing failure, tap changer failure, core failure, tank leaks
- **Breakers**: SF6 gas loss, mechanism failure, contact wear, vacuum bottle failure, control circuit failure
- **Lines**: Conductor failure, insulator failure, tower/pole failure, cable insulation failure, joint failure
- **Switches**: Contact deterioration, mechanism binding, insulation tracking

### 3. Physics-Based Degradation Models
- **Weibull Distribution**: Time-to-failure with shape (β) and scale (η) parameters
- **Arrhenius Thermal Model**: Temperature-accelerated aging with activation energy
- **NOT age-based**: Uses actual operating conditions and physics

### 4. Network-Aware Data Model
- Network nodes (buses, substations, junctions)
- Network edges (lines, cables with impedance)
- Switching paths (alternative feeds, restoration times)
- Customer impact mapping (downstream tracing)

### 5. Monetized Risk ($)
- Customer interruption costs
- Safety incident costs
- Regulatory fines
- Environmental remediation
- Equipment damage
- Reputation damage
- Network reconfiguration costs

## The 6-Layer Risk Framework

```
Layer 6: Portfolio Optimization
    ↓
Layer 5: Intervention Economics
    ↓
Layer 4: Monetized Consequence ($)
    ↓
Layer 3: Network Impact (connectivity)
    ↓
Layer 2: Asset Condition (Weibull/Arrhenius)
    ↓
Layer 1: Asset Inventory (T&D taxonomy)
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Run with Docker Compose

```bash
# Clone and navigate to project
cd aip-core

# Start all services
docker-compose up -d

# Wait for database initialization (30-60 seconds)
docker-compose logs -f postgres

# Access API documentation
open http://localhost:8000/docs

# Access PGAdmin (optional)
open http://localhost:5050
# Login: admin@aip.local / admin
```

### Local Development

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://aip_user:aip_password@localhost:5432/aip_db"

# Run migrations and start server
uvicorn app.main:app --reload
```

## API Endpoints

### Assets
- `GET /api/v1/assets` - List all assets
- `GET /api/v1/assets/{id}` - Get asset details
- `POST /api/v1/assets` - Create new asset
- `GET /api/v1/assets/summary` - Asset health summary
- `GET /api/v1/assets/types` - Asset types (taxonomy)
- `GET /api/v1/assets/failure-modes` - Failure mode catalog

### Network
- `GET /api/v1/network/nodes` - Network nodes
- `GET /api/v1/network/edges` - Network edges
- `GET /api/v1/network/connectivity` - Connectivity view
- `POST /api/v1/network/analyze` - Run network analysis
- `GET /api/v1/network/asset/{id}/downstream-customers` - Customer impact

### Risk
- `GET /api/v1/risk/summary` - Risk summary for all assets
- `POST /api/v1/risk/calculate` - Calculate risk for asset
- `POST /api/v1/risk/calculate-all` - Calculate risk for all assets
- `GET /api/v1/risk/top-risk-assets` - Highest risk assets
- `POST /api/v1/risk/calculate-consequence/{id}` - Calculate monetized consequence

### Condition
- `GET /api/v1/condition/assessments` - Condition assessments
- `POST /api/v1/condition/assessments` - Create assessment
- `GET /api/v1/condition/diagnostic-tests` - Diagnostic test results
- `GET /api/v1/condition/asset/{id}/dga-latest` - Latest DGA results
- `GET /api/v1/condition/asset/{id}/health-trend` - Health score trend

### Investment
- `GET /api/v1/investment/interventions` - Intervention options
- `GET /api/v1/investment/projects` - Investment projects
- `POST /api/v1/investment/projects` - Create project
- `POST /api/v1/investment/optimize` - Run portfolio optimization
- `GET /api/v1/investment/dashboard` - Investment dashboard

## Database Schema

The system includes 18+ tables:

| Table | Purpose |
|-------|---------|
| `asset_types` | T&D-specific taxonomy |
| `assets` | Core asset register |
| `asset_locations` | Geographic information |
| `failure_modes` | Failure mechanism catalog |
| `degradation_models` | Physics-based models (Weibull, Arrhenius) |
| `survival_models` | Statistical survival analysis |
| `network_nodes` | Topology nodes |
| `network_edges` | Connections |
| `switching_paths` | Alternative feeds |
| `condition_assessments` | Health assessments |
| `diagnostic_tests` | DGA, oil quality, etc. |
| `monitoring_data` | Real-time data |
| `customer_connections` | Customer impact mapping |
| `consequence_profiles` | Monetized consequences ($) |
| `risk_calculations` | Risk quantification |
| `intervention_options` | Investment options |
| `investment_projects` | Approved projects |
| `portfolio_scenarios` | Optimization scenarios |

## Sample Data

The system includes 50 realistic T&D assets:
- 15 Transformers (power and distribution)
- 12 Circuit Breakers (SF6 and vacuum)
- 10 Lines (overhead and underground)
- 8 Switches
- 5 Other equipment

With realistic:
- Failure modes and degradation models
- Condition assessments and DGA results
- Network connectivity and switching paths
- Customer impact data
- Risk calculations
- Intervention options

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                       │
├─────────────────────────────────────────────────────────────┤
│  Routers  →  Services  →  Models  →  PostgreSQL/PostGIS     │
│  (API)       (Logic)      (ORM)       (Database)            │
├─────────────────────────────────────────────────────────────┤
│  • Risk Calculator (Weibull/Arrhenius)                      │
│  • Network Analyzer (connectivity, switching)               │
│  • Portfolio Optimizer (knapsack, MILP)                     │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | postgresql://... | PostgreSQL connection string |
| `DEBUG` | false | Enable debug mode |
| `DEFAULT_TIME_HORIZON_YEARS` | 10 | Default risk analysis period |
| `DEFAULT_DISCOUNT_RATE` | 0.07 | NPV discount rate |

## License

MIT License - See LICENSE file for details.
