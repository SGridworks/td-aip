-- T&D Asset Investment Planning (AIP) - PostgreSQL Schema
-- Physics-based degradation models, network-aware, monetized risk

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- ============================================================================
-- LAYER 1: ASSET INVENTORY TABLES
-- ============================================================================

-- T&D-specific asset taxonomy (NOT generic assets)
CREATE TABLE asset_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(50) NOT NULL CHECK (category IN (
        'TRANSFORMER', 'BREAKER', 'LINE', 'SWITCH', 
        'REGULATOR', 'CAPACITOR', 'RECLOSER', 'SECTIONALIZER'
    )),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    voltage_classes VARCHAR(20)[],
    typical_lifespan_years INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE asset_types IS 'T&D-specific asset taxonomy - transformers, breakers, lines, switches, etc.';

-- Geographic and service territory information
CREATE TABLE asset_locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    substation_id VARCHAR(50) NOT NULL,
    substation_name VARCHAR(200),
    latitude DECIMAL(10,8) CHECK (latitude BETWEEN -90 AND 90),
    longitude DECIMAL(11,8) CHECK (longitude BETWEEN -180 AND 180),
    voltage_level VARCHAR(20),
    service_territory VARCHAR(100),
    climate_zone VARCHAR(50),
    geom GEOMETRY(POINT, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_asset_locations_geom ON asset_locations USING GIST(geom);

-- Core asset register
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_type_id UUID NOT NULL REFERENCES asset_types(id),
    location_id UUID REFERENCES asset_locations(id),
    name VARCHAR(200) NOT NULL,
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    install_date DATE NOT NULL,
    mva_rating DECIMAL(10,3),
    voltage_primary_kv DECIMAL(8,3),
    voltage_secondary_kv DECIMAL(8,3),
    health_score DECIMAL(4,3) CHECK (health_score BETWEEN 0 AND 1),
    criticality INTEGER CHECK (criticality BETWEEN 1 AND 5),
    status VARCHAR(20) DEFAULT 'IN_SERVICE' CHECK (status IN ('IN_SERVICE', 'OUT_OF_SERVICE', 'PLANNED', 'RETIRED')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assets_type ON assets(asset_type_id);
CREATE INDEX idx_assets_location ON assets(location_id);
CREATE INDEX idx_assets_health ON assets(health_score);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_assets_install_date ON assets(install_date);

-- ============================================================================
-- LAYER 2: FAILURE MODE & DEGRADATION MODEL TABLES
-- ============================================================================

-- T&D-specific failure mechanisms catalog
CREATE TABLE failure_modes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_type_id UUID NOT NULL REFERENCES asset_types(id),
    failure_category VARCHAR(50) NOT NULL CHECK (failure_category IN ('MAJOR', 'CATASTROPHIC', 'DEGRADED', 'INCIDENTAL')),
    mechanism VARCHAR(100) NOT NULL,
    description TEXT,
    typical_causes TEXT[],
    precursors TEXT[],
    failure_rate_base DECIMAL(10,6), -- Annual failure rate
    repair_cost_avg DECIMAL(12,2), -- Average repair cost ($)
    replacement_cost_avg DECIMAL(12,2), -- Average replacement cost ($)
    outage_hours_avg DECIMAL(6,2), -- Average outage duration
    safety_risk INTEGER CHECK (safety_risk BETWEEN 1 AND 5),
    environmental_risk INTEGER CHECK (environmental_risk BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_failure_modes_type ON failure_modes(asset_type_id);
CREATE INDEX idx_failure_modes_category ON failure_modes(failure_category);

COMMENT ON TABLE failure_modes IS 'T&D-specific failure modes: oil degradation, winding failure, bushing failure, etc.';

-- Physics-based degradation models (NOT age-based)
CREATE TABLE degradation_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    failure_mode_id UUID NOT NULL REFERENCES failure_modes(id),
    model_type VARCHAR(50) NOT NULL CHECK (model_type IN ('WEIBULL', 'ARRHENIUS', 'COFFIN_MANSON', 'EYE_CHART', 'MARKOV')),
    -- Weibull parameters for time-to-failure
    weibull_shape DECIMAL(8,4), -- β (shape parameter)
    weibull_scale DECIMAL(8,4), -- η (scale parameter in years)
    weibull_location DECIMAL(8,4), -- γ (location parameter)
    -- Arrhenius parameters for thermal degradation
    arrhenius_pre_exp DECIMAL(20,10), -- A (pre-exponential factor)
    arrhenius_activation_ev DECIMAL(8,4), -- Ea (activation energy in eV)
    temp_reference_c DECIMAL(6,2), -- Reference temperature
    -- Condition-based thresholds
    condition_thresholds JSONB, -- Threshold values for condition states
    -- Model metadata
    model_equation TEXT, -- Mathematical formulation
    calibration_data_source TEXT,
    validation_status VARCHAR(20) DEFAULT 'PENDING' CHECK (validation_status IN ('VALIDATED', 'PENDING', 'EXPERIMENTAL')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_degradation_models_failure_mode ON degradation_models(failure_mode_id);
CREATE INDEX idx_degradation_models_type ON degradation_models(model_type);

COMMENT ON TABLE degradation_models IS 'Physics-based degradation: Weibull, Arrhenius thermal models, NOT age-based';

-- Statistical survival analysis for asset populations
CREATE TABLE survival_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    failure_mode_id UUID NOT NULL REFERENCES failure_modes(id),
    model_type VARCHAR(50) NOT NULL CHECK (model_type IN ('KAPLAN_MEIER', 'COX_PH', 'WEIBULL_REG', 'LOG_NORMAL')),
    covariates JSONB, -- Predictor variables used (e.g., ["age", "load_factor", "temperature"])
    baseline_hazard JSONB, -- Baseline hazard function parameters
    regression_coefficients JSONB, -- Model coefficients
    confidence_level DECIMAL(3,2) DEFAULT 0.95,
    sample_size INTEGER,
    calibration_date DATE,
    next_calibration_due DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- LAYER 3: NETWORK CONNECTIVITY TABLES
-- ============================================================================

-- Network topology nodes (buses, substations, connection points)
CREATE TABLE network_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID REFERENCES assets(id),
    node_type VARCHAR(50) NOT NULL CHECK (node_type IN ('BUS', 'SUBSTATION', 'TAP_POINT', 'JUNCTION', 'LOAD_CENTER')),
    name VARCHAR(200) NOT NULL,
    voltage_level VARCHAR(20),
    operational_state VARCHAR(20) DEFAULT 'ACTIVE' CHECK (operational_state IN ('ACTIVE', 'OUTAGE', 'MAINTENANCE', 'PLANNED')),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    geom GEOMETRY(POINT, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_network_nodes_asset ON network_nodes(asset_id);
CREATE INDEX idx_network_nodes_geom ON network_nodes USING GIST(geom);
CREATE INDEX idx_network_nodes_type ON network_nodes(node_type);

-- Network connections (lines, cables)
CREATE TABLE network_edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_node_id UUID NOT NULL REFERENCES network_nodes(id),
    to_node_id UUID NOT NULL REFERENCES network_nodes(id),
    asset_id UUID REFERENCES assets(id),
    edge_type VARCHAR(50) NOT NULL CHECK (edge_type IN ('OVERHEAD', 'UNDERGROUND', 'CABLE', 'SUBSTATION_BUS')),
    length_km DECIMAL(8,3),
    impedance_r DECIMAL(10,6), -- Resistance (ohms)
    impedance_x DECIMAL(10,6), -- Reactance (ohms)
    thermal_rating_mva DECIMAL(8,3),
    emergency_rating_mva DECIMAL(8,3),
    geom GEOMETRY(LINESTRING, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_network_edges_from ON network_edges(from_node_id);
CREATE INDEX idx_network_edges_to ON network_edges(to_node_id);
CREATE INDEX idx_network_edges_asset ON network_edges(asset_id);
CREATE INDEX idx_network_edges_geom ON network_edges USING GIST(geom);

-- Alternative feed paths for restoration
CREATE TABLE switching_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_node_id UUID NOT NULL REFERENCES network_nodes(id),
    target_node_id UUID NOT NULL REFERENCES network_nodes(id),
    path_geometry GEOMETRY(LINESTRING, 4326),
    path_distance_km DECIMAL(8,3),
    switching_time_min INTEGER, -- Time to switch load (minutes)
    backup_capacity_mva DECIMAL(8,3), -- Available backup capacity
    switching_devices UUID[], -- Array of switch asset IDs
    automatic_switching BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_switching_paths_source ON switching_paths(source_node_id);
CREATE INDEX idx_switching_paths_target ON switching_paths(target_node_id);

COMMENT ON TABLE switching_paths IS 'Network-aware switching paths for restoration analysis';

-- ============================================================================
-- LAYER 4: CONDITION ASSESSMENT TABLES
-- ============================================================================

-- Asset condition evaluation records
CREATE TABLE condition_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id),
    assessment_date DATE NOT NULL,
    assessor VARCHAR(100),
    assessment_type VARCHAR(50) CHECK (assessment_type IN ('VISUAL', 'DIAGNOSTIC', 'ONLINE', 'OFFLINE')),
    overall_condition INTEGER CHECK (overall_condition BETWEEN 1 AND 5), -- 5=excellent
    health_index DECIMAL(4,3) CHECK (health_index BETWEEN 0 AND 1),
    probability_of_failure DECIMAL(8,6), -- Annual PoF
    remaining_life_years DECIMAL(6,2),
    next_assessment_due DATE,
    confidence_score DECIMAL(3,2),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_condition_assessments_asset ON condition_assessments(asset_id);
CREATE INDEX idx_condition_assessments_date ON condition_assessments(assessment_date);

-- Laboratory and field test results
CREATE TABLE diagnostic_tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id),
    test_date DATE NOT NULL,
    test_type VARCHAR(50) NOT NULL CHECK (test_type IN (
        'DGA', 'OIL_QUALITY', 'INSULATION_PF', 'WINDING_RES', 
        'TURNS_RATIO', 'THERMOGRAPHY', 'SF6_QUALITY', 'CONTACT_RESISTANCE'
    )),
    -- Oil quality metrics
    oil_dielectric_strength DECIMAL(6,2), -- kV breakdown
    oil_moisture_ppm DECIMAL(8,2), -- Moisture content
    oil_acidity DECIMAL(6,4), -- Neutralization number (mg KOH/g)
    oil_interfacial_tension DECIMAL(6,2), -- mN/m
    -- Dissolved Gas Analysis (DGA)
    dissolved_gases JSONB, -- {H2, CH4, C2H6, C2H4, C2H2, CO, CO2, total}
    dga_key_gas VARCHAR(20), -- Dominant gas
    dga_rogers_ratio INTEGER, -- Rogers ratio code
    -- Insulation tests
    insulation_power_factor DECIMAL(6,4), -- % power factor
    insulation_resistance_gohm DECIMAL(10,2), -- GΩ
    -- Winding tests
    winding_resistance JSONB, -- Resistance measurements by phase {A: ohms, B: ohms, C: ohms}
    turns_ratio_deviation DECIMAL(6,4), -- % deviation
    -- Thermography
    temperature_rise DECIMAL(6,2), -- Temperature increase (°C)
    thermography_findings JSONB, -- Hot spot temperatures and locations
    -- SF6 (for breakers)
    sf6_purity_percent DECIMAL(5,2),
    sf6_dew_point_c DECIMAL(6,2),
    -- Overall result
    overall_test_result VARCHAR(20) CHECK (overall_test_result IN ('PASS', 'FAIL', 'CAUTION', 'INCONCLUSIVE')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_diagnostic_tests_asset ON diagnostic_tests(asset_id);
CREATE INDEX idx_diagnostic_tests_date ON diagnostic_tests(test_date);
CREATE INDEX idx_diagnostic_tests_type ON diagnostic_tests(test_type);

-- Real-time and periodic monitoring data
CREATE TABLE monitoring_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    sensor_type VARCHAR(50) CHECK (sensor_type IN ('TEMPERATURE', 'LOAD', 'OIL_LEVEL', 'VIBRATION', 'PD', 'GAS', 'DISSOLVED_GAS')),
    -- Temperature measurements
    temperature_top_oil_c DECIMAL(6,2),
    temperature_winding_c DECIMAL(6,2),
    temperature_ambient_c DECIMAL(6,2),
    -- Load measurements
    load_mva DECIMAL(8,3),
    load_percent DECIMAL(6,2), -- % of rated load
    -- Oil measurements
    oil_level_percent DECIMAL(6,2),
    oil_temperature_c DECIMAL(6,2),
    -- Vibration
    vibration_mm_s DECIMAL(6,3), -- Vibration velocity mm/s
    -- Partial discharge
    partial_discharge_pc DECIMAL(10,2), -- PD magnitude (pC)
    partial_discharge_pattern VARCHAR(50),
    -- Gas pressure (SF6)
    gas_pressure_kpa DECIMAL(8,2),
    gas_pressure_normalized_kpa DECIMAL(8,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_monitoring_data_asset_time ON monitoring_data(asset_id, timestamp);
CREATE INDEX idx_monitoring_data_timestamp ON monitoring_data(timestamp);

-- ============================================================================
-- LAYER 5: CUSTOMER & CONSEQUENCE TABLES (MONETIZED)
-- ============================================================================

-- Customer impact mapping
CREATE TABLE customer_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id),
    downstream_asset_id UUID REFERENCES assets(id),
    customers_served INTEGER DEFAULT 0,
    critical_customers INTEGER DEFAULT 0,
    peak_load_mw DECIMAL(8,3),
    average_load_mw DECIMAL(8,3),
    -- Critical facilities
    hospitals_served INTEGER DEFAULT 0,
    schools_served INTEGER DEFAULT 0,
    emergency_services INTEGER DEFAULT 0,
    water_wastewater_facilities INTEGER DEFAULT 0,
    communication_towers INTEGER DEFAULT 0,
    -- Load breakdown
    industrial_mw DECIMAL(8,3),
    commercial_mw DECIMAL(8,3),
    residential_mw DECIMAL(8,3),
    agricultural_mw DECIMAL(8,3),
    -- Outage costs
    avg_outage_cost_per_hour DECIMAL(10,2), -- $/hour
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customer_connections_asset ON customer_connections(asset_id);
CREATE INDEX idx_customer_connections_downstream ON customer_connections(downstream_asset_id);

COMMENT ON TABLE customer_connections IS 'Network-aware customer impact mapping';

-- Monetized consequence values (NOT scores)
CREATE TABLE consequence_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id),
    calculation_date DATE NOT NULL,
    -- Customer interruption costs
    customer_interruption_cost DECIMAL(12,2), -- $ value of customer outages
    customer_interruption_cost_hourly DECIMAL(12,2), -- $/hour
    -- Safety costs
    safety_incident_probability DECIMAL(8,6),
    safety_incident_cost DECIMAL(12,2), -- $ expected safety cost
    -- Regulatory costs
    regulatory_fine_probability DECIMAL(8,6),
    regulatory_fine_cost DECIMAL(12,2), -- $ expected regulatory penalties
    -- Environmental costs
    environmental_remediation_cost DECIMAL(12,2), -- $ cleanup
    spill_volume_estimate_liters DECIMAL(10,2),
    -- Equipment costs
    equipment_repair_cost DECIMAL(12,2),
    equipment_replacement_cost DECIMAL(12,2),
    -- Network costs
    network_reconfiguration_cost DECIMAL(12,2), -- $ switching/restoration
    -- Reputation
    reputation_damage_cost DECIMAL(12,2),
    -- Totals
    total_consequence_per_event DECIMAL(12,2), -- Sum of all consequences
    annual_expected_consequence DECIMAL(12,2), -- Annual expected value
    currency VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_consequence_profiles_asset ON consequence_profiles(asset_id);
CREATE INDEX idx_consequence_profiles_date ON consequence_profiles(calculation_date);

COMMENT ON TABLE consequence_profiles IS 'MONETIZED risk consequences in $, NOT scores';

-- ============================================================================
-- LAYER 6: RISK CALCULATION TABLES
-- ============================================================================

-- Risk quantification results
CREATE TABLE risk_calculations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id),
    calculation_date DATE NOT NULL,
    scenario_type VARCHAR(50) DEFAULT 'BASE_CASE' CHECK (scenario_type IN ('BASE_CASE', 'STRESSED', 'PLANNED', 'OPTIMISTIC')),
    time_horizon_years INTEGER DEFAULT 5,
    -- Failure probabilities
    annual_failure_probability DECIMAL(10,8), -- PoF per year
    cumulative_failure_prob DECIMAL(10,8), -- Cumulative PoF over horizon
    -- Expected costs
    expected_annual_cost DECIMAL(12,2), -- $ annual expected cost
    expected_lifecycle_cost DECIMAL(14,2), -- $ over time horizon
    -- Risk metrics
    risk_adjusted_npv DECIMAL(14,2),
    value_at_risk_95 DECIMAL(12,2),
    conditional_var_95 DECIMAL(12,2),
    -- Confidence
    confidence_interval_lower DECIMAL(10,8),
    confidence_interval_upper DECIMAL(10,8),
    confidence_level DECIMAL(3,2) DEFAULT 0.95,
    -- Assumptions
    key_assumptions JSONB,
    calculation_method VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_risk_calculations_asset ON risk_calculations(asset_id);
CREATE INDEX idx_risk_calculations_date ON risk_calculations(calculation_date);
CREATE INDEX idx_risk_calculations_scenario ON risk_calculations(scenario_type);

-- ============================================================================
-- LAYER 7: INVESTMENT & PORTFOLIO TABLES
-- ============================================================================

-- Possible investment interventions
CREATE TABLE intervention_options (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id),
    intervention_type VARCHAR(50) NOT NULL CHECK (intervention_type IN (
        'REPLACE', 'REFURBISH_MAJOR', 'REFURBISH_MINOR', 
        'MONITOR_ENHANCE', 'MAINTAIN_PREVENTIVE', 'DECOMMISSION', 'DEFER'
    )),
    description TEXT,
    cost_estimate DECIMAL(12,2), -- Estimated cost ($)
    cost_uncertainty_percent DECIMAL(5,2), -- Cost uncertainty (%)
    implementation_time_months INTEGER,
    -- Risk reduction
    risk_reduction_percent DECIMAL(6,2), -- % risk reduction achieved
    failure_probability_reduction DECIMAL(8,6), -- Absolute PoF reduction
    -- Life extension
    life_extension_years DECIMAL(6,2), -- Years of life added
    reliability_improvement_factor DECIMAL(6,3),
    -- Priority
    priority_score DECIMAL(8,4), -- Calculated priority
    benefit_cost_ratio DECIMAL(8,4),
    status VARCHAR(20) DEFAULT 'PROPOSED' CHECK (status IN ('PROPOSED', 'APPROVED', 'REJECTED', 'IMPLEMENTED')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_intervention_options_asset ON intervention_options(asset_id);
CREATE INDEX idx_intervention_options_priority ON intervention_options(priority_score DESC);
CREATE INDEX idx_intervention_options_status ON intervention_options(status);

-- Approved investment projects
CREATE TABLE investment_projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_name VARCHAR(200) NOT NULL,
    project_type VARCHAR(50) CHECK (project_type IN ('ASSET_REPLACEMENT', 'REFURBISHMENT', 'EXPANSION', 'RELIABILITY', 'MONITORING')),
    budget_year INTEGER NOT NULL,
    total_budget DECIMAL(12,2) NOT NULL,
    risk_reduction_total DECIMAL(12,2), -- Total risk reduction ($)
    implementation_year INTEGER,
    completion_year INTEGER,
    status VARCHAR(20) DEFAULT 'PLANNED' CHECK (status IN ('PLANNED', 'APPROVED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    priority_rank INTEGER,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_investment_projects_year ON investment_projects(budget_year);
CREATE INDEX idx_investment_projects_status ON investment_projects(status);

-- Link interventions to projects
CREATE TABLE project_interventions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES investment_projects(id),
    intervention_id UUID NOT NULL REFERENCES intervention_options(id),
    allocated_budget DECIMAL(12,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Investment portfolio optimization scenarios
CREATE TABLE portfolio_scenarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scenario_name VARCHAR(200) NOT NULL,
    budget_constraint DECIMAL(14,2), -- Total budget limit
    risk_tolerance DECIMAL(12,2), -- Acceptable risk level
    time_horizon_years INTEGER DEFAULT 10,
    selected_projects UUID[], -- Array of project IDs
    total_investment DECIMAL(14,2),
    total_risk_reduction DECIMAL(14,2),
    expected_roi DECIMAL(8,4),
    risk_adjusted_return DECIMAL(8,4),
    optimization_date DATE,
    optimization_method VARCHAR(50),
    constraints JSONB, -- Optimization constraints
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Asset health summary view
CREATE VIEW asset_health_summary AS
SELECT 
    a.id,
    a.name,
    at.category AS asset_type,
    at.name AS type_name,
    a.install_date,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, a.install_date)) AS age_years,
    a.health_score,
    a.criticality,
    a.status,
    al.substation_name,
    al.service_territory,
    ca.overall_condition,
    ca.remaining_life_years,
    ca.probability_of_failure,
    cc.customers_served,
    cc.peak_load_mw
FROM assets a
JOIN asset_types at ON a.asset_type_id = at.id
LEFT JOIN asset_locations al ON a.location_id = al.id
LEFT JOIN LATERAL (
    SELECT * FROM condition_assessments ca 
    WHERE ca.asset_id = a.id 
    ORDER BY ca.assessment_date DESC 
    LIMIT 1
) ca ON true
LEFT JOIN customer_connections cc ON a.id = cc.asset_id;

-- Risk summary view
CREATE VIEW risk_summary AS
SELECT 
    a.id AS asset_id,
    a.name AS asset_name,
    at.category AS asset_type,
    rc.calculation_date,
    rc.annual_failure_probability,
    rc.cumulative_failure_prob,
    rc.expected_annual_cost,
    cp.total_consequence_per_event,
    (rc.annual_failure_probability * cp.total_consequence_per_event) AS annual_risk_exposure,
    cc.customers_served,
    cc.critical_customers
FROM assets a
JOIN asset_types at ON a.asset_type_id = at.id
LEFT JOIN LATERAL (
    SELECT * FROM risk_calculations rc 
    WHERE rc.asset_id = a.id AND rc.scenario_type = 'BASE_CASE'
    ORDER BY rc.calculation_date DESC 
    LIMIT 1
) rc ON true
LEFT JOIN LATERAL (
    SELECT * FROM consequence_profiles cp 
    WHERE cp.asset_id = a.id
    ORDER BY cp.calculation_date DESC 
    LIMIT 1
) cp ON true
LEFT JOIN customer_connections cc ON a.id = cc.asset_id;

-- Network connectivity view
CREATE VIEW network_connectivity AS
SELECT 
    ne.id AS edge_id,
    ne.edge_type,
    ne.length_km,
    ne.thermal_rating_mva,
    fn.id AS from_node_id,
    fn.name AS from_node_name,
    fn.voltage_level AS from_voltage,
    tn.id AS to_node_id,
    tn.name AS to_node_name,
    tn.voltage_level AS to_voltage,
    fa.id AS from_asset_id,
    fa.name AS from_asset_name,
    ta.id AS to_asset_id,
    ta.name AS to_asset_name
FROM network_edges ne
JOIN network_nodes fn ON ne.from_node_id = fn.id
JOIN network_nodes tn ON ne.to_node_id = tn.id
LEFT JOIN assets fa ON fn.asset_id = fa.id
LEFT JOIN assets ta ON tn.asset_id = ta.id;

-- ============================================================================
-- FUNCTIONS FOR RISK CALCULATIONS
-- ============================================================================

-- Calculate Weibull failure probability
CREATE OR REPLACE FUNCTION calculate_weibull_pof(
    age_years DECIMAL,
    shape_beta DECIMAL,
    scale_eta DECIMAL,
    location_gamma DECIMAL DEFAULT 0
) RETURNS DECIMAL AS $$
DECLARE
    adjusted_age DECIMAL;
    reliability DECIMAL;
BEGIN
    IF age_years <= location_gamma THEN
        RETURN 0;
    END IF;
    adjusted_age := age_years - location_gamma;
    reliability := EXP(-POWER(adjusted_age / scale_eta, shape_beta));
    RETURN 1 - reliability;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Calculate Arrhenius thermal aging acceleration factor
CREATE OR REPLACE FUNCTION calculate_arrhenius_af(
    actual_temp_c DECIMAL,
    reference_temp_c DECIMAL,
    activation_energy_ev DECIMAL
) RETURNS DECIMAL AS $$
DECLARE
    boltzmann_ev_per_k DECIMAL := 8.617333262e-5;
    actual_temp_k DECIMAL;
    reference_temp_k DECIMAL;
BEGIN
    actual_temp_k := actual_temp_c + 273.15;
    reference_temp_k := reference_temp_c + 273.15;
    RETURN EXP((activation_energy_ev / boltzmann_ev_per_k) * (1/reference_temp_k - 1/actual_temp_k));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Calculate monetized risk
CREATE OR REPLACE FUNCTION calculate_monetized_risk(
    failure_probability DECIMAL,
    consequence_cost DECIMAL
) RETURNS DECIMAL AS $$
BEGIN
    RETURN failure_probability * consequence_cost;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Update asset health score trigger
CREATE OR REPLACE FUNCTION update_asset_health_score()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE assets 
    SET health_score = NEW.health_index,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.asset_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_asset_health
AFTER INSERT OR UPDATE ON condition_assessments
FOR EACH ROW
EXECUTE FUNCTION update_asset_health_score();

-- Update timestamps trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_assets_updated_at
BEFORE UPDATE ON assets
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
