"""
SQLAlchemy ORM models for AIP Core
"""

from sqlalchemy import Column, String, DateTime, Date, DECIMAL, Integer, Boolean, Text, ForeignKey, ARRAY, JSONB
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class AssetType(Base):
    """T&D-specific asset taxonomy."""
    __tablename__ = "asset_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    voltage_classes = Column(ARRAY(String(20)))
    typical_lifespan_years = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    assets = relationship("Asset", back_populates="asset_type")
    failure_modes = relationship("FailureMode", back_populates="asset_type")


class AssetLocation(Base):
    """Geographic and service territory information."""
    __tablename__ = "asset_locations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    substation_id = Column(String(50), nullable=False)
    substation_name = Column(String(200))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    voltage_level = Column(String(20))
    service_territory = Column(String(100))
    climate_zone = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    assets = relationship("Asset", back_populates="location")


class Asset(Base):
    """Core asset register."""
    __tablename__ = "assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_type_id = Column(UUID(as_uuid=True), ForeignKey("asset_types.id"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("asset_locations.id"))
    name = Column(String(200), nullable=False)
    manufacturer = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    install_date = Column(Date, nullable=False)
    mva_rating = Column(DECIMAL(10, 3))
    voltage_primary_kv = Column(DECIMAL(8, 3))
    voltage_secondary_kv = Column(DECIMAL(8, 3))
    health_score = Column(DECIMAL(4, 3))
    criticality = Column(Integer)
    status = Column(String(20), default='IN_SERVICE')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    asset_type = relationship("AssetType", back_populates="assets")
    location = relationship("AssetLocation", back_populates="assets")
    condition_assessments = relationship("ConditionAssessment", back_populates="asset")
    diagnostic_tests = relationship("DiagnosticTest", back_populates="asset")
    monitoring_data = relationship("MonitoringData", back_populates="asset")
    customer_connections = relationship("CustomerConnection", back_populates="asset")
    risk_calculations = relationship("RiskCalculation", back_populates="asset")
    intervention_options = relationship("InterventionOption", back_populates="asset")


class FailureMode(Base):
    """T&D-specific failure mechanisms catalog."""
    __tablename__ = "failure_modes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_type_id = Column(UUID(as_uuid=True), ForeignKey("asset_types.id"), nullable=False)
    failure_category = Column(String(50), nullable=False)
    mechanism = Column(String(100), nullable=False)
    description = Column(Text)
    typical_causes = Column(ARRAY(Text))
    precursors = Column(ARRAY(Text))
    failure_rate_base = Column(DECIMAL(10, 6))
    repair_cost_avg = Column(DECIMAL(12, 2))
    replacement_cost_avg = Column(DECIMAL(12, 2))
    outage_hours_avg = Column(DECIMAL(6, 2))
    safety_risk = Column(Integer)
    environmental_risk = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    asset_type = relationship("AssetType", back_populates="failure_modes")
    degradation_models = relationship("DegradationModel", back_populates="failure_mode")
    survival_models = relationship("SurvivalModel", back_populates="failure_mode")


class DegradationModel(Base):
    """Physics-based degradation models."""
    __tablename__ = "degradation_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    failure_mode_id = Column(UUID(as_uuid=True), ForeignKey("failure_modes.id"), nullable=False)
    model_type = Column(String(50), nullable=False)
    # Weibull parameters
    weibull_shape = Column(DECIMAL(8, 4))
    weibull_scale = Column(DECIMAL(8, 4))
    weibull_location = Column(DECIMAL(8, 4))
    # Arrhenius parameters
    arrhenius_pre_exp = Column(DECIMAL(20, 10))
    arrhenius_activation_ev = Column(DECIMAL(8, 4))
    temp_reference_c = Column(DECIMAL(6, 2))
    condition_thresholds = Column(JSONB)
    model_equation = Column(Text)
    calibration_data_source = Column(Text)
    validation_status = Column(String(20), default='PENDING')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    failure_mode = relationship("FailureMode", back_populates="degradation_models")


class SurvivalModel(Base):
    """Statistical survival analysis."""
    __tablename__ = "survival_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    failure_mode_id = Column(UUID(as_uuid=True), ForeignKey("failure_modes.id"), nullable=False)
    model_type = Column(String(50), nullable=False)
    covariates = Column(JSONB)
    baseline_hazard = Column(JSONB)
    regression_coefficients = Column(JSONB)
    confidence_level = Column(DECIMAL(3, 2), default=0.95)
    sample_size = Column(Integer)
    calibration_date = Column(Date)
    next_calibration_due = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    failure_mode = relationship("FailureMode", back_populates="survival_models")


class NetworkNode(Base):
    """Network topology nodes."""
    __tablename__ = "network_nodes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"))
    node_type = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)
    voltage_level = Column(String(20))
    operational_state = Column(String(20), default='ACTIVE')
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class NetworkEdge(Base):
    """Network connections."""
    __tablename__ = "network_edges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_node_id = Column(UUID(as_uuid=True), ForeignKey("network_nodes.id"), nullable=False)
    to_node_id = Column(UUID(as_uuid=True), ForeignKey("network_nodes.id"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"))
    edge_type = Column(String(50), nullable=False)
    length_km = Column(DECIMAL(8, 3))
    impedance_r = Column(DECIMAL(10, 6))
    impedance_x = Column(DECIMAL(10, 6))
    thermal_rating_mva = Column(DECIMAL(8, 3))
    emergency_rating_mva = Column(DECIMAL(8, 3))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SwitchingPath(Base):
    """Alternative feed paths for restoration."""
    __tablename__ = "switching_paths"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_node_id = Column(UUID(as_uuid=True), ForeignKey("network_nodes.id"), nullable=False)
    target_node_id = Column(UUID(as_uuid=True), ForeignKey("network_nodes.id"), nullable=False)
    path_distance_km = Column(DECIMAL(8, 3))
    switching_time_min = Column(Integer)
    backup_capacity_mva = Column(DECIMAL(8, 3))
    switching_devices = Column(ARRAY(UUID(as_uuid=True)))
    automatic_switching = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ConditionAssessment(Base):
    """Asset condition evaluation records."""
    __tablename__ = "condition_assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    assessment_date = Column(Date, nullable=False)
    assessor = Column(String(100))
    assessment_type = Column(String(50))
    overall_condition = Column(Integer)
    health_index = Column(DECIMAL(4, 3))
    probability_of_failure = Column(DECIMAL(8, 6))
    remaining_life_years = Column(DECIMAL(6, 2))
    next_assessment_due = Column(Date)
    confidence_score = Column(DECIMAL(3, 2))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    asset = relationship("Asset", back_populates="condition_assessments")


class DiagnosticTest(Base):
    """Laboratory and field test results."""
    __tablename__ = "diagnostic_tests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    test_date = Column(Date, nullable=False)
    test_type = Column(String(50), nullable=False)
    oil_dielectric_strength = Column(DECIMAL(6, 2))
    oil_moisture_ppm = Column(DECIMAL(8, 2))
    oil_acidity = Column(DECIMAL(6, 4))
    oil_interfacial_tension = Column(DECIMAL(6, 2))
    dissolved_gases = Column(JSONB)
    dga_key_gas = Column(String(20))
    dga_rogers_ratio = Column(Integer)
    insulation_power_factor = Column(DECIMAL(6, 4))
    winding_resistance = Column(JSONB)
    turns_ratio_deviation = Column(DECIMAL(6, 4))
    temperature_rise = Column(DECIMAL(6, 2))
    thermography_findings = Column(JSONB)
    sf6_purity_percent = Column(DECIMAL(5, 2))
    sf6_dew_point_c = Column(DECIMAL(6, 2))
    overall_test_result = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    asset = relationship("Asset", back_populates="diagnostic_tests")


class MonitoringData(Base):
    """Real-time and periodic monitoring data."""
    __tablename__ = "monitoring_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    sensor_type = Column(String(50))
    temperature_top_oil_c = Column(DECIMAL(6, 2))
    temperature_winding_c = Column(DECIMAL(6, 2))
    temperature_ambient_c = Column(DECIMAL(6, 2))
    load_mva = Column(DECIMAL(8, 3))
    load_percent = Column(DECIMAL(6, 2))
    oil_level_percent = Column(DECIMAL(6, 2))
    oil_temperature_c = Column(DECIMAL(6, 2))
    vibration_mm_s = Column(DECIMAL(6, 3))
    partial_discharge_pc = Column(DECIMAL(10, 2))
    partial_discharge_pattern = Column(String(50))
    gas_pressure_kpa = Column(DECIMAL(8, 2))
    gas_pressure_normalized_kpa = Column(DECIMAL(8, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    asset = relationship("Asset", back_populates="monitoring_data")


class CustomerConnection(Base):
    """Customer impact mapping."""
    __tablename__ = "customer_connections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    downstream_asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"))
    customers_served = Column(Integer, default=0)
    critical_customers = Column(Integer, default=0)
    peak_load_mw = Column(DECIMAL(8, 3))
    average_load_mw = Column(DECIMAL(8, 3))
    hospitals_served = Column(Integer, default=0)
    schools_served = Column(Integer, default=0)
    emergency_services = Column(Integer, default=0)
    water_wastewater_facilities = Column(Integer, default=0)
    communication_towers = Column(Integer, default=0)
    industrial_mw = Column(DECIMAL(8, 3))
    commercial_mw = Column(DECIMAL(8, 3))
    residential_mw = Column(DECIMAL(8, 3))
    agricultural_mw = Column(DECIMAL(8, 3))
    avg_outage_cost_per_hour = Column(DECIMAL(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    asset = relationship("Asset", foreign_keys=[asset_id], back_populates="customer_connections")


class ConsequenceProfile(Base):
    """Monetized consequence values."""
    __tablename__ = "consequence_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    calculation_date = Column(Date, nullable=False)
    customer_interruption_cost = Column(DECIMAL(12, 2))
    customer_interruption_cost_hourly = Column(DECIMAL(12, 2))
    safety_incident_probability = Column(DECIMAL(8, 6))
    safety_incident_cost = Column(DECIMAL(12, 2))
    regulatory_fine_probability = Column(DECIMAL(8, 6))
    regulatory_fine_cost = Column(DECIMAL(12, 2))
    environmental_remediation_cost = Column(DECIMAL(12, 2))
    spill_volume_estimate_liters = Column(DECIMAL(10, 2))
    equipment_repair_cost = Column(DECIMAL(12, 2))
    equipment_replacement_cost = Column(DECIMAL(12, 2))
    network_reconfiguration_cost = Column(DECIMAL(12, 2))
    reputation_damage_cost = Column(DECIMAL(12, 2))
    total_consequence_per_event = Column(DECIMAL(12, 2))
    annual_expected_consequence = Column(DECIMAL(12, 2))
    currency = Column(String(3), default='USD')
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RiskCalculation(Base):
    """Risk quantification results."""
    __tablename__ = "risk_calculations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    calculation_date = Column(Date, nullable=False)
    scenario_type = Column(String(50), default='BASE_CASE')
    time_horizon_years = Column(Integer, default=5)
    annual_failure_probability = Column(DECIMAL(10, 8))
    cumulative_failure_prob = Column(DECIMAL(10, 8))
    expected_annual_cost = Column(DECIMAL(12, 2))
    expected_lifecycle_cost = Column(DECIMAL(14, 2))
    risk_adjusted_npv = Column(DECIMAL(14, 2))
    value_at_risk_95 = Column(DECIMAL(12, 2))
    conditional_var_95 = Column(DECIMAL(12, 2))
    confidence_interval_lower = Column(DECIMAL(10, 8))
    confidence_interval_upper = Column(DECIMAL(10, 8))
    confidence_level = Column(DECIMAL(3, 2), default=0.95)
    key_assumptions = Column(JSONB)
    calculation_method = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    asset = relationship("Asset", back_populates="risk_calculations")


class InterventionOption(Base):
    """Possible investment interventions."""
    __tablename__ = "intervention_options"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    intervention_type = Column(String(50), nullable=False)
    description = Column(Text)
    cost_estimate = Column(DECIMAL(12, 2))
    cost_uncertainty_percent = Column(DECIMAL(5, 2))
    implementation_time_months = Column(Integer)
    risk_reduction_percent = Column(DECIMAL(6, 2))
    failure_probability_reduction = Column(DECIMAL(8, 6))
    life_extension_years = Column(DECIMAL(6, 2))
    reliability_improvement_factor = Column(DECIMAL(6, 3))
    priority_score = Column(DECIMAL(8, 4))
    benefit_cost_ratio = Column(DECIMAL(8, 4))
    status = Column(String(20), default='PROPOSED')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    asset = relationship("Asset", back_populates="intervention_options")


class InvestmentProject(Base):
    """Approved investment projects."""
    __tablename__ = "investment_projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = Column(String(200), nullable=False)
    project_type = Column(String(50))
    budget_year = Column(Integer, nullable=False)
    total_budget = Column(DECIMAL(12, 2), nullable=False)
    risk_reduction_total = Column(DECIMAL(12, 2))
    implementation_year = Column(Integer)
    completion_year = Column(Integer)
    status = Column(String(20), default='PLANNED')
    priority_rank = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PortfolioScenario(Base):
    """Investment portfolio optimization scenarios."""
    __tablename__ = "portfolio_scenarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_name = Column(String(200), nullable=False)
    budget_constraint = Column(DECIMAL(14, 2))
    risk_tolerance = Column(DECIMAL(12, 2))
    time_horizon_years = Column(Integer, default=10)
    selected_projects = Column(ARRAY(UUID(as_uuid=True)))
    total_investment = Column(DECIMAL(14, 2))
    total_risk_reduction = Column(DECIMAL(14, 2))
    expected_roi = Column(DECIMAL(8, 4))
    risk_adjusted_return = Column(DECIMAL(8, 4))
    optimization_date = Column(Date)
    optimization_method = Column(String(50))
    constraints = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
