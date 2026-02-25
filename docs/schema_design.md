# T&D Asset Investment Planning (AIP) - Core Database Schema

## Overview
This database schema implements a T&D-specific Asset Investment Planning tool with:
- T&D-specific asset taxonomy (transformers, breakers, lines, switches)
- Failure mode catalog with physics-based degradation models
- Network-aware connectivity model
- Monetized risk calculations

## Schema Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CORE ASSET TABLES                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────┐ │
│  │ asset_types     │    │ assets           │    │ asset_locations         │ │
│  │ ─────────────   │    │ ───────────────  │    │ ─────────────────────   │ │
│  │ id (PK)         │◄───┤ asset_type_id    │    │ id (PK)                 │ │
│  │ category        │    │ location_id (FK) │───►│ substation_id           │ │
│  │ name            │    │ name, mva_rating │    │ latitude, longitude     │ │
│  │ description     │    │ install_date     │    │ voltage_level           │ │
│  │ voltage_classes │    │ health_score     │    │ service_territory       │ │
│  └─────────────────┘    │ criticality      │    └─────────────────────────┘ │
│                         └──────────────────┘                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      NETWORK CONNECTIVITY MODEL                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌──────────────────┐    ┌────────────────────────┐ │
│  │ network_nodes    │    │ network_edges    │    │ switching_paths        │ │
│  │ ───────────────  │    │ ───────────────  │    │ ─────────────────────  │ │
│  │ id (PK)          │    │ id (PK)          │    │ id (PK)                │ │
│  │ asset_id (FK)    │◄───┤ from_node_id     │◄───┤ source_node_id (FK)    │ │
│  │ node_type        │    │ to_node_id       │    │ target_node_id (FK)    │ │
│  │ voltage_level    │    │ edge_type        │    │ path_geometry          │ │
│  │ operational_state│    │ length_km        │    │ switching_time_min     │ │
│  └──────────────────┘    │ impedance        │    │ alternative_feed       │ │
│                          │ thermal_rating   │    │ backup_capacity_mva    │ │
│                          └──────────────────┘    └────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     FAILURE MODE & DEGRADATION MODELS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐   ┌─────────────────────┐   ┌────────────────────┐ │
│  │ failure_modes       │   │ degradation_models  │   │ survival_models    │ │
│  │ ─────────────────   │   │ ─────────────────── │   │ ─────────────────  │ │
│  │ id (PK)             │   │ id (PK)             │   │ id (PK)            │ │
│  │ asset_type_id (FK)  │   │ failure_mode_id(FK) │   │ failure_mode_id(FK)│ │
│  │ failure_category    │   │ model_type          │   │ model_type         │ │
│  │ mechanism           │   │ weibull_shape (β)   │   │ weibull_shape      │ │
│  │ description         │   │ weibull_scale (η)   │   │ weibull_scale      │ │
│  │ typical_causes      │   │ arrhenius_a         │   │ covariates         │ │
│  │ failure_rate_base   │   │ arrhenius_ea        │   │ calibration_date   │ │
│  │ repair_cost_avg     │   │ temp_reference      │   │ confidence_level   │ │
│  │ outage_hours_avg    │   │ condition_thresholds│   │ sample_size        │ │
│  └─────────────────────┘   └─────────────────────┘   └────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONDITION ASSESSMENT & MONITORING                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐   ┌─────────────────────┐   ┌────────────────────┐ │
│  │ condition_assessments│  │ diagnostic_tests    │   │ monitoring_data    │ │
│  │ ─────────────────── │   │ ─────────────────── │   │ ─────────────────  │ │
│  │ id (PK)             │   │ id (PK)             │   │ id (PK)            │ │
│  │ asset_id (FK)       │   │ asset_id (FK)       │   │ asset_id (FK)      │ │
│  │ assessment_date     │   │ test_date           │   │ timestamp          │ │
│  │ assessor            │   │ test_type           │   │ sensor_type        │ │
│  │ overall_condition   │   │ oil_quality_metrics │   │ temperature_c      │ │
│  │ health_index        │   │ dissolved_gases     │   │ load_mva           │ │
│  │ remaining_life_yrs  │   │ insulation_pf       │   │ oil_level          │ │
│  │ next_assessment_due │   │ winding_resistance  │   │ vibration          │ │
│  │ confidence_score    │   │ turns_ratio         │   │ partial_discharge  │ │
│  └─────────────────────┘   └─────────────────────┘   └────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      CUSTOMER & CONSEQUENCE MODEL                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐   ┌─────────────────────┐   ┌────────────────────┐ │
│  │ customer_connections│   │ consequence_profiles│   │ risk_calculations  │ │
│  │ ─────────────────── │   │ ─────────────────── │   │ ─────────────────  │ │
│  │ id (PK)             │   │ id (PK)             │   │ id (PK)            │ │
│  │ asset_id (FK)       │   │ asset_id (FK)       │   │ asset_id (FK)      │ │
│  │ customers_served    │   │ interruption_cost   │   │ calculation_date   │ │
│  │ critical_load_mw    │   │ safety_incident_cost│   │ annual_failure_prob│ │
│  │ hospitals_served    │   │ regulatory_fine_risk│   │ expected_annual_cost││
│  │ schools_served      │   │ reputation_damage   │   │ risk_adjusted_npv  │ │
│  │ emergency_services  │   │ environmental_cost  │   │ confidence_interval│ │
│  │ avg_outage_cost     │   │ total_consequence_$ │   │ scenario_type      │ │
│  └─────────────────────┘   └─────────────────────┘   └────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      INVESTMENT & PORTFOLIO TABLES                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐   ┌─────────────────────┐   ┌────────────────────┐ │
│  │ intervention_options│   │ investment_projects │   │ portfolio_scenarios│ │
│  │ ─────────────────── │   │ ─────────────────── │   │ ─────────────────  │ │
│  │ id (PK)             │   │ id (PK)             │   │ id (PK)            │ │
│  │ asset_id (FK)       │   │ project_name        │   │ scenario_name      │ │
│  │ intervention_type   │   │ budget_year         │   │ budget_constraint  │ │
│  │ cost_estimate       │   │ total_budget        │   │ risk_tolerance     │ │
│  │ risk_reduction      │   │ risk_reduction_total│   │ selected_projects  │ │
│  │ life_extension_yrs  │   │ implementation_year │   │ expected_roi       │ │
│  │ implementation_time │   │ status              │   │ risk_reduction_ach │ │
│  │ priority_score      │   │ priority_rank       │   │ optimization_date  │ │
│  └─────────────────────┘   └─────────────────────┘   └────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## The 6-Layer Risk Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         6-LAYER RISK FRAMEWORK                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER 6: Portfolio Optimization                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Multi-asset investment decisions under budget & risk constraints    │   │
│  │ Output: Optimal project portfolio, risk-adjusted NPV                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│  LAYER 5: Intervention Economics    │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Cost-benefit of replacement, refurbishment, monitoring enhancements │   │
│  │ Output: Intervention priority scores, risk reduction curves         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│  LAYER 4: Monetized Consequence     │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Customer impact, safety, regulatory, environmental costs in $       │   │
│  │ Output: Total consequence value per failure event                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│  LAYER 3: Network Impact            │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Connectivity analysis, switching paths, load transfer capability    │   │
│  │ Output: Customers affected, load at risk, restoration time          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│  LAYER 2: Asset Condition           │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Physics-based degradation models (Weibull, Arrhenius)               │   │
│  │ Output: Failure probability, remaining useful life                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│  LAYER 1: Asset Inventory           │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ T&D-specific taxonomy, locations, ratings, connectivity             │   │
│  │ Output: Asset register with network topology                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Table Definitions

### 1. asset_types
T&D-specific asset taxonomy - NOT generic assets

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| category | VARCHAR(50) | TRANSFORMER, BREAKER, LINE, SWITCH, REGULATOR, CAPACITOR, RECLOSER, SECTIONALIZER |
| name | VARCHAR(100) | Specific type name |
| description | TEXT | Detailed description |
| voltage_classes | VARCHAR[] | Array of applicable voltage levels (e.g., ['12kV', '34.5kV']) |
| typical_lifespan_years | INTEGER | Expected service life |
| created_at | TIMESTAMP | Record creation time |

### 2. assets
Core asset register

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_type_id | UUID FK | Reference to asset_types |
| location_id | UUID FK | Reference to asset_locations |
| name | VARCHAR(200) | Asset identifier/name |
| manufacturer | VARCHAR(100) | Equipment manufacturer |
| model | VARCHAR(100) | Model number |
| serial_number | VARCHAR(100) | Serial number |
| install_date | DATE | Installation date |
| mva_rating | DECIMAL | MVA capacity rating |
| voltage_primary_kv | DECIMAL | Primary voltage (kV) |
| voltage_secondary_kv | DECIMAL | Secondary voltage (kV) |
| health_score | DECIMAL(3,2) | 0.00-1.00 health index |
| criticality | INTEGER | 1-5 criticality ranking |
| status | VARCHAR(20) | IN_SERVICE, OUT_OF_SERVICE, PLANNED |
| created_at | TIMESTAMP | Record creation time |

### 3. asset_locations
Geographic and service territory information

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| substation_id | VARCHAR(50) | Substation identifier |
| substation_name | VARCHAR(200) | Substation name |
| latitude | DECIMAL(10,8) | GPS latitude |
| longitude | DECIMAL(11,8) | GPS longitude |
| voltage_level | VARCHAR(20) | Voltage class at location |
| service_territory | VARCHAR(100) | Service area/region |
| climate_zone | VARCHAR(50) | Environmental classification |
| created_at | TIMESTAMP | Record creation time |

### 4. failure_modes
T&D-specific failure mechanisms catalog

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_type_id | UUID FK | Applicable asset type |
| failure_category | VARCHAR(50) | MAJOR, CATASTROPHIC, DEGRADED |
| mechanism | VARCHAR(100) | Specific failure mechanism |
| description | TEXT | Detailed description |
| typical_causes | TEXT[] | Array of common causes |
| precursors | TEXT[] | Warning signs/indicators |
| failure_rate_base | DECIMAL | Base annual failure rate |
| repair_cost_avg | DECIMAL | Average repair cost ($) |
| replacement_cost_avg | DECIMAL | Average replacement cost ($) |
| outage_hours_avg | DECIMAL | Average outage duration |
| safety_risk | INTEGER | 1-5 safety risk rating |
| environmental_risk | INTEGER | 1-5 environmental risk rating |
| created_at | TIMESTAMP | Record creation time |

**Key T&D Failure Modes:**
- **Transformers:** Oil degradation, winding failure, bushing failure, tap changer failure, core failure, tank/pipe leaks
- **Circuit Breakers:** Mechanism failure, insulation failure, contact wear, SF6 leaks, control circuit failure
- **Lines:** Conductor fatigue, insulator failure, tower/pole decay, galloping, vegetation contact, lightning damage
- **Switches:** Contact deterioration, mechanism binding, insulation tracking, heating at joints

### 5. degradation_models
Physics-based degradation models (NOT age-based)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| failure_mode_id | UUID FK | Associated failure mode |
| model_type | VARCHAR(50) | WEIBULL, ARRHENIUS, COFFIN_MANSON, EYE_CHART |
| weibull_shape | DECIMAL | Weibull shape parameter (β) |
| weibull_scale | DECIMAL | Weibull scale parameter (η) in years |
| arrhenius_pre_exp | DECIMAL | Arrhenius pre-exponential factor (A) |
| arrhenius_activation_ev | DECIMAL | Activation energy in eV |
| temp_reference_c | DECIMAL | Reference temperature (°C) |
| condition_thresholds | JSONB | Threshold values for condition states |
| model_equation | TEXT | Mathematical formulation |
| calibration_data_source | TEXT | Source of calibration data |
| validation_status | VARCHAR(20) | VALIDATED, PENDING, EXPERIMENTAL |
| created_at | TIMESTAMP | Record creation time |

**Model Types:**
- **Weibull:** Time-to-failure distribution for random failures
- **Arrhenius:** Temperature-accelerated degradation (thermal aging)
- **Coffin-Manson:** Thermal cycling fatigue
- **Eye-Chart:** Condition-based transition matrices

### 6. survival_models
Statistical survival analysis for asset populations

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| failure_mode_id | UUID FK | Associated failure mode |
| model_type | VARCHAR(50) | KAPLAN_MEIER, COX_PH, WEIBULL_REG |
| covariates | JSONB | Predictor variables used |
| baseline_hazard | JSONB | Baseline hazard function |
| regression_coefficients | JSONB | Model coefficients |
| confidence_level | DECIMAL | Statistical confidence (e.g., 0.95) |
| sample_size | INTEGER | Number of observations |
| calibration_date | DATE | Model calibration date |
| next_calibration_due | DATE | Next calibration due |
| created_at | TIMESTAMP | Record creation time |

### 7. network_nodes
Network topology nodes (buses, substations, connection points)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_id | UUID FK | Associated asset (if applicable) |
| node_type | VARCHAR(50) | BUS, SUBSTATION, TAP_POINT, JUNCTION |
| name | VARCHAR(200) | Node identifier |
| voltage_level | VARCHAR(20) | Operating voltage |
| operational_state | VARCHAR(20) | ACTIVE, OUTAGE, MAINTENANCE |
| latitude | DECIMAL(10,8) | GPS latitude |
| longitude | DECIMAL(11,8) | GPS longitude |
| created_at | TIMESTAMP | Record creation time |

### 8. network_edges
Network connections (lines, cables)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| from_node_id | UUID FK | Source node |
| to_node_id | UUID FK | Destination node |
| asset_id | UUID FK | Associated line/cable asset |
| edge_type | VARCHAR(50) | OVERHEAD, UNDERGROUND, CABLE |
| length_km | DECIMAL | Line length in kilometers |
| impedance_r | DECIMAL | Resistance (ohms) |
| impedance_x | DECIMAL | Reactance (ohms) |
| thermal_rating_mva | DECIMAL | Thermal capacity (MVA) |
| emergency_rating_mva | DECIMAL | Emergency capacity (MVA) |
| created_at | TIMESTAMP | Record creation time |

### 9. switching_paths
Alternative feed paths for restoration

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| source_node_id | UUID FK | Normal source node |
| target_node_id | UUID FK | Alternative source node |
| path_geometry | GEOMETRY | Line path (PostGIS) |
| path_distance_km | DECIMAL | Path length |
| switching_time_min | INTEGER | Time to switch load (minutes) |
| backup_capacity_mva | DECIMAL | Available backup capacity |
| switching_devices | UUID[] | Array of switch asset IDs |
| automatic_switching | BOOLEAN | Auto-transfer capable |
| created_at | TIMESTAMP | Record creation time |

### 10. condition_assessments
Asset condition evaluation records

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_id | UUID FK | Assessed asset |
| assessment_date | DATE | Assessment date |
| assessor | VARCHAR(100) | Assessor name/organization |
| assessment_type | VARCHAR(50) | VISUAL, DIAGNOSTIC, ONLINE |
| overall_condition | INTEGER | 1-5 condition grade (5=excellent) |
| health_index | DECIMAL(4,3) | 0.000-1.000 health score |
| probability_of_failure | DECIMAL | Annual PoF |
| remaining_life_years | DECIMAL | Estimated RUL |
| next_assessment_due | DATE | Next assessment date |
| confidence_score | DECIMAL | Assessment confidence |
| notes | TEXT | Additional notes |
| created_at | TIMESTAMP | Record creation time |

### 11. diagnostic_tests
Laboratory and field test results

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_id | UUID FK | Tested asset |
| test_date | DATE | Test date |
| test_type | VARCHAR(50) | DGA, OIL_QUALITY, INSULATION_PF, WINDING_RES, TURNS_RATIO, THERMOGRAPHY |
| oil_dielectric_strength | DECIMAL | kV breakdown |
| oil_moisture_ppm | DECIMAL | Moisture content |
| oil_acidity | DECIMAL | Neutralization number |
| dissolved_gases | JSONB | DGA results (H2, CH4, C2H6, C2H4, C2H2, CO, CO2) |
| insulation_power_factor | DECIMAL | % power factor |
| winding_resistance | JSONB | Resistance measurements by phase |
| turns_ratio_deviation | DECIMAL | % deviation |
| temperature_rise | DECIMAL | Temperature increase (°C) |
| thermography_findings | JSONB | Hot spot temperatures |
| overall_test_result | VARCHAR(20) | PASS, FAIL, CAUTION |
| created_at | TIMESTAMP | Record creation time |

### 12. monitoring_data
Real-time and periodic monitoring data

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_id | UUID FK | Monitored asset |
| timestamp | TIMESTAMP | Measurement time |
| sensor_type | VARCHAR(50) | TEMPERATURE, LOAD, OIL_LEVEL, VIBRATION, PD, GAS |
| temperature_top_oil_c | DECIMAL | Top oil temperature |
| temperature_winding_c | DECIMAL | Winding temperature |
| ambient_temperature_c | DECIMAL | Ambient temperature |
| load_mva | DECIMAL | Current load |
| load_percent | DECIMAL | % of rated load |
| oil_level_percent | DECIMAL | Oil level indicator |
| vibration_mm_s | DECIMAL | Vibration velocity |
| partial_discharge_pc | DECIMAL | PD magnitude (pC) |
| gas_pressure_kpa | DECIMAL | SF6/gas pressure |
| created_at | TIMESTAMP | Record creation time |

### 13. customer_connections
Customer impact mapping

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_id | UUID FK | Supplying asset |
| downstream_asset_id | UUID FK | Next downstream asset |
| customers_served | INTEGER | Number of customers |
| critical_customers | INTEGER | Critical load customers |
| peak_load_mw | DECIMAL | Peak demand |
| average_load_mw | DECIMAL | Average demand |
| hospitals_served | INTEGER | Count of hospitals |
| schools_served | INTEGER | Count of schools |
| emergency_services | INTEGER | Count of emergency facilities |
| industrial_mw | DECIMAL | Industrial load |
| commercial_mw | DECIMAL | Commercial load |
| residential_mw | DECIMAL | Residential load |
| created_at | TIMESTAMP | Record creation time |

### 14. consequence_profiles
Monetized consequence values (NOT scores)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_id | UUID FK | Asset reference |
| calculation_date | DATE | Calculation date |
| customer_interruption_cost | DECIMAL | $ value of customer outages |
| safety_incident_cost | DECIMAL | $ value of safety risk |
| regulatory_fine_risk | DECIMAL | $ expected regulatory penalties |
| environmental_remediation | DECIMAL | $ environmental cleanup |
| equipment_damage_cost | DECIMAL | $ equipment replacement/repair |
| reputation_damage | DECIMAL | $ reputational impact |
| network_reconfiguration_cost | DECIMAL | $ switching/restoration costs |
| total_consequence_per_event | DECIMAL | Sum of all consequences |
| annual_expected_consequence | DECIMAL | Annual expected value |
| currency | VARCHAR(3) | USD, EUR, etc. |
| created_at | TIMESTAMP | Record creation time |

### 15. risk_calculations
Risk quantification results

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_id | UUID FK | Asset reference |
| calculation_date | DATE | Calculation date |
| scenario_type | VARCHAR(50) | BASE_CASE, STRESSED, PLANNED |
| time_horizon_years | INTEGER | Analysis period |
| annual_failure_probability | DECIMAL | PoF per year |
| cumulative_failure_prob | DECIMAL | Cumulative PoF over horizon |
| expected_annual_cost | DECIMAL | $ annual expected cost |
| risk_adjusted_npv | DECIMAL | Risk-adjusted net present value |
| confidence_interval_lower | DECIMAL | Lower confidence bound |
| confidence_interval_upper | DECIMAL | Upper confidence bound |
| key_assumptions | JSONB | Calculation assumptions |
| created_at | TIMESTAMP | Record creation time |

### 16. intervention_options
Possible investment interventions

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| asset_id | UUID FK | Target asset |
| intervention_type | VARCHAR(50) | REPLACE, REFURBISH, MONITOR, MAINTAIN, DECOMMISSION |
| description | TEXT | Detailed description |
| cost_estimate | DECIMAL | Estimated cost ($) |
| cost_uncertainty | DECIMAL | Cost uncertainty (%) |
| implementation_time_months | INTEGER | Time to implement |
| risk_reduction_percent | DECIMAL | % risk reduction achieved |
| life_extension_years | DECIMAL | Years of life added |
| reliability_improvement | DECIMAL | Reliability improvement factor |
| priority_score | DECIMAL | Calculated priority |
| status | VARCHAR(20) | PROPOSED, APPROVED, REJECTED |
| created_at | TIMESTAMP | Record creation time |

### 17. investment_projects
Approved investment projects

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| project_name | VARCHAR(200) | Project name |
| project_type | VARCHAR(50) | ASSET_REPLACEMENT, REFURBISHMENT, EXPANSION |
| budget_year | INTEGER | Fiscal year |
| total_budget | DECIMAL | Total project budget |
| risk_reduction_total | DECIMAL | Total risk reduction ($) |
| implementation_year | INTEGER | Planned year |
| completion_year | INTEGER | Expected completion |
| status | VARCHAR(20) | PLANNED, IN_PROGRESS, COMPLETED |
| priority_rank | INTEGER | Portfolio priority |
| created_at | TIMESTAMP | Record creation time |

### 18. portfolio_scenarios
Investment portfolio optimization scenarios

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Unique identifier |
| scenario_name | VARCHAR(200) | Scenario name |
| budget_constraint | DECIMAL | Total budget limit |
| risk_tolerance | DECIMAL | Acceptable risk level |
| time_horizon_years | INTEGER | Planning period |
| selected_projects | UUID[] | Array of project IDs |
| total_investment | DECIMAL | Sum of selected investments |
| total_risk_reduction | DECIMAL | Total risk reduction achieved |
| expected_roi | DECIMAL | Expected return on investment |
| risk_adjusted_return | DECIMAL | Risk-adjusted return |
| optimization_date | DATE | When optimized |
| optimization_method | VARCHAR(50) | OPTIMIZATION method used |
| created_at | TIMESTAMP | Record creation time |

## Indexes

```sql
-- Performance indexes for common query patterns
CREATE INDEX idx_assets_type ON assets(asset_type_id);
CREATE INDEX idx_assets_location ON assets(location_id);
CREATE INDEX idx_assets_health ON assets(health_score);
CREATE INDEX idx_assets_status ON assets(status);

CREATE INDEX idx_failure_modes_type ON failure_modes(asset_type_id);
CREATE INDEX idx_failure_modes_category ON failure_modes(failure_category);

CREATE INDEX idx_network_edges_from ON network_edges(from_node_id);
CREATE INDEX idx_network_edges_to ON network_edges(to_node_id);
CREATE INDEX idx_network_edges_asset ON network_edges(asset_id);

CREATE INDEX idx_condition_assessments_asset ON condition_assessments(asset_id);
CREATE INDEX idx_condition_assessments_date ON condition_assessments(assessment_date);

CREATE INDEX idx_monitoring_data_asset_time ON monitoring_data(asset_id, timestamp);

CREATE INDEX idx_customer_connections_asset ON customer_connections(asset_id);
CREATE INDEX idx_risk_calculations_asset ON risk_calculations(asset_id);
CREATE INDEX idx_intervention_options_asset ON intervention_options(asset_id);
CREATE INDEX idx_intervention_options_priority ON intervention_options(priority_score DESC);
```

## Relationships Summary

```
asset_types 1───* assets *───1 asset_locations
                   │
                   ├───* failure_modes
                   │       └───* degradation_models
                   │       └───* survival_models
                   │
                   ├───* condition_assessments
                   ├───* diagnostic_tests
                   ├───* monitoring_data
                   │
                   ├───* customer_connections
                   │       └───* consequence_profiles
                   │
                   ├───* risk_calculations
                   │
                   ├───* intervention_options
                   │       └───* investment_projects
                   │
                   └───1 network_nodes *───* network_edges
                           │
                           └───* switching_paths
```
