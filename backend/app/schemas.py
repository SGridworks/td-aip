"""
Pydantic schemas for API request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


# ============================================================================
# Asset Schemas
# ============================================================================

class AssetTypeBase(BaseModel):
    category: str
    name: str
    description: Optional[str] = None
    voltage_classes: Optional[List[str]] = None
    typical_lifespan_years: Optional[int] = None


class AssetTypeCreate(AssetTypeBase):
    pass


class AssetTypeResponse(AssetTypeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime


class AssetLocationBase(BaseModel):
    substation_id: str
    substation_name: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    voltage_level: Optional[str] = None
    service_territory: Optional[str] = None
    climate_zone: Optional[str] = None


class AssetLocationCreate(AssetLocationBase):
    pass


class AssetLocationResponse(AssetLocationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime


class AssetBase(BaseModel):
    name: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    install_date: date
    mva_rating: Optional[Decimal] = None
    voltage_primary_kv: Optional[Decimal] = None
    voltage_secondary_kv: Optional[Decimal] = None
    health_score: Optional[Decimal] = Field(None, ge=0, le=1)
    criticality: Optional[int] = Field(None, ge=1, le=5)
    status: str = "IN_SERVICE"


class AssetCreate(AssetBase):
    asset_type_id: UUID
    location_id: Optional[UUID] = None


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    health_score: Optional[Decimal] = Field(None, ge=0, le=1)
    criticality: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None


class AssetResponse(AssetBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_type_id: UUID
    location_id: Optional[UUID] = None
    asset_type: Optional[AssetTypeResponse] = None
    location: Optional[AssetLocationResponse] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class AssetHealthSummary(BaseModel):
    """Asset health summary view schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    asset_type: str
    type_name: str
    install_date: date
    age_years: Optional[float] = None
    health_score: Optional[Decimal] = None
    criticality: Optional[int] = None
    status: str
    substation_name: Optional[str] = None
    service_territory: Optional[str] = None
    overall_condition: Optional[int] = None
    remaining_life_years: Optional[Decimal] = None
    probability_of_failure: Optional[Decimal] = None
    customers_served: Optional[int] = None
    peak_load_mw: Optional[Decimal] = None


# ============================================================================
# Failure Mode Schemas
# ============================================================================

class FailureModeBase(BaseModel):
    failure_category: str
    mechanism: str
    description: Optional[str] = None
    typical_causes: Optional[List[str]] = None
    precursors: Optional[List[str]] = None
    failure_rate_base: Optional[Decimal] = None
    repair_cost_avg: Optional[Decimal] = None
    replacement_cost_avg: Optional[Decimal] = None
    outage_hours_avg: Optional[Decimal] = None
    safety_risk: Optional[int] = Field(None, ge=1, le=5)
    environmental_risk: Optional[int] = Field(None, ge=1, le=5)


class FailureModeCreate(FailureModeBase):
    asset_type_id: UUID


class FailureModeResponse(FailureModeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_type_id: UUID
    created_at: datetime


class DegradationModelBase(BaseModel):
    model_type: str
    weibull_shape: Optional[Decimal] = None
    weibull_scale: Optional[Decimal] = None
    weibull_location: Optional[Decimal] = None
    arrhenius_pre_exp: Optional[Decimal] = None
    arrhenius_activation_ev: Optional[Decimal] = None
    temp_reference_c: Optional[Decimal] = None
    condition_thresholds: Optional[Dict[str, Any]] = None
    model_equation: Optional[str] = None
    calibration_data_source: Optional[str] = None
    validation_status: str = "PENDING"


class DegradationModelCreate(DegradationModelBase):
    failure_mode_id: UUID


class DegradationModelResponse(DegradationModelBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    failure_mode_id: UUID
    created_at: datetime


# ============================================================================
# Network Schemas
# ============================================================================

class NetworkNodeBase(BaseModel):
    node_type: str
    name: str
    voltage_level: Optional[str] = None
    operational_state: str = "ACTIVE"
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class NetworkNodeCreate(NetworkNodeBase):
    asset_id: Optional[UUID] = None


class NetworkNodeResponse(NetworkNodeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_id: Optional[UUID] = None
    created_at: datetime


class NetworkEdgeBase(BaseModel):
    edge_type: str
    length_km: Optional[Decimal] = None
    impedance_r: Optional[Decimal] = None
    impedance_x: Optional[Decimal] = None
    thermal_rating_mva: Optional[Decimal] = None
    emergency_rating_mva: Optional[Decimal] = None


class NetworkEdgeCreate(NetworkEdgeBase):
    from_node_id: UUID
    to_node_id: UUID
    asset_id: Optional[UUID] = None


class NetworkEdgeResponse(NetworkEdgeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    from_node_id: UUID
    to_node_id: UUID
    asset_id: Optional[UUID] = None
    created_at: datetime


class SwitchingPathBase(BaseModel):
    path_distance_km: Optional[Decimal] = None
    switching_time_min: Optional[int] = None
    backup_capacity_mva: Optional[Decimal] = None
    switching_devices: Optional[List[UUID]] = None
    automatic_switching: bool = False
    is_active: bool = True


class SwitchingPathCreate(SwitchingPathBase):
    source_node_id: UUID
    target_node_id: UUID


class SwitchingPathResponse(SwitchingPathBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    source_node_id: UUID
    target_node_id: UUID
    created_at: datetime


class NetworkConnectivity(BaseModel):
    """Network connectivity view schema."""
    model_config = ConfigDict(from_attributes=True)
    
    edge_id: UUID
    edge_type: str
    length_km: Optional[Decimal] = None
    thermal_rating_mva: Optional[Decimal] = None
    from_node_id: UUID
    from_node_name: str
    from_voltage: Optional[str] = None
    to_node_id: UUID
    to_node_name: str
    to_voltage: Optional[str] = None
    from_asset_id: Optional[UUID] = None
    from_asset_name: Optional[str] = None
    to_asset_id: Optional[UUID] = None
    to_asset_name: Optional[str] = None


class NetworkAnalysisRequest(BaseModel):
    """Request for network analysis."""
    node_id: UUID
    analysis_type: str = "connectivity"  # connectivity, switching_paths, load_flow
    max_depth: int = 5


class NetworkAnalysisResponse(BaseModel):
    """Response from network analysis."""
    node_id: UUID
    analysis_type: str
    connected_nodes: List[Dict[str, Any]]
    switching_options: Optional[List[Dict[str, Any]]] = None
    customers_at_risk: Optional[int] = None
    load_at_risk_mw: Optional[Decimal] = None


# ============================================================================
# Condition Assessment Schemas
# ============================================================================

class ConditionAssessmentBase(BaseModel):
    assessment_date: date
    assessor: Optional[str] = None
    assessment_type: Optional[str] = None
    overall_condition: Optional[int] = Field(None, ge=1, le=5)
    health_index: Optional[Decimal] = Field(None, ge=0, le=1)
    probability_of_failure: Optional[Decimal] = None
    remaining_life_years: Optional[Decimal] = None
    next_assessment_due: Optional[date] = None
    confidence_score: Optional[Decimal] = None
    notes: Optional[str] = None


class ConditionAssessmentCreate(ConditionAssessmentBase):
    asset_id: UUID


class ConditionAssessmentResponse(ConditionAssessmentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_id: UUID
    created_at: datetime


class DiagnosticTestBase(BaseModel):
    test_date: date
    test_type: str
    oil_dielectric_strength: Optional[Decimal] = None
    oil_moisture_ppm: Optional[Decimal] = None
    oil_acidity: Optional[Decimal] = None
    oil_interfacial_tension: Optional[Decimal] = None
    dissolved_gases: Optional[Dict[str, Any]] = None
    dga_key_gas: Optional[str] = None
    dga_rogers_ratio: Optional[int] = None
    insulation_power_factor: Optional[Decimal] = None
    winding_resistance: Optional[Dict[str, Any]] = None
    turns_ratio_deviation: Optional[Decimal] = None
    temperature_rise: Optional[Decimal] = None
    overall_test_result: Optional[str] = None


class DiagnosticTestCreate(DiagnosticTestBase):
    asset_id: UUID


class DiagnosticTestResponse(DiagnosticTestBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_id: UUID
    created_at: datetime


class MonitoringDataBase(BaseModel):
    timestamp: datetime
    sensor_type: Optional[str] = None
    temperature_top_oil_c: Optional[Decimal] = None
    temperature_winding_c: Optional[Decimal] = None
    temperature_ambient_c: Optional[Decimal] = None
    load_mva: Optional[Decimal] = None
    load_percent: Optional[Decimal] = None
    oil_level_percent: Optional[Decimal] = None
    partial_discharge_pc: Optional[Decimal] = None
    gas_pressure_kpa: Optional[Decimal] = None


class MonitoringDataCreate(MonitoringDataBase):
    asset_id: UUID


class MonitoringDataResponse(MonitoringDataBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_id: UUID
    created_at: datetime


# ============================================================================
# Risk Calculation Schemas
# ============================================================================

class CustomerConnectionBase(BaseModel):
    customers_served: int = 0
    critical_customers: int = 0
    peak_load_mw: Optional[Decimal] = None
    average_load_mw: Optional[Decimal] = None
    hospitals_served: int = 0
    schools_served: int = 0
    emergency_services: int = 0
    industrial_mw: Optional[Decimal] = None
    commercial_mw: Optional[Decimal] = None
    residential_mw: Optional[Decimal] = None
    avg_outage_cost_per_hour: Optional[Decimal] = None


class CustomerConnectionCreate(CustomerConnectionBase):
    asset_id: UUID
    downstream_asset_id: Optional[UUID] = None


class CustomerConnectionResponse(CustomerConnectionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_id: UUID
    downstream_asset_id: Optional[UUID] = None
    created_at: datetime


class ConsequenceProfileBase(BaseModel):
    calculation_date: date
    customer_interruption_cost: Optional[Decimal] = None
    customer_interruption_cost_hourly: Optional[Decimal] = None
    safety_incident_probability: Optional[Decimal] = None
    safety_incident_cost: Optional[Decimal] = None
    regulatory_fine_probability: Optional[Decimal] = None
    regulatory_fine_cost: Optional[Decimal] = None
    environmental_remediation_cost: Optional[Decimal] = None
    equipment_repair_cost: Optional[Decimal] = None
    equipment_replacement_cost: Optional[Decimal] = None
    network_reconfiguration_cost: Optional[Decimal] = None
    reputation_damage_cost: Optional[Decimal] = None
    total_consequence_per_event: Optional[Decimal] = None
    annual_expected_consequence: Optional[Decimal] = None
    currency: str = "USD"


class ConsequenceProfileCreate(ConsequenceProfileBase):
    asset_id: UUID


class ConsequenceProfileResponse(ConsequenceProfileBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_id: UUID
    created_at: datetime


class RiskCalculationBase(BaseModel):
    calculation_date: date
    scenario_type: str = "BASE_CASE"
    time_horizon_years: int = 5
    annual_failure_probability: Optional[Decimal] = None
    cumulative_failure_prob: Optional[Decimal] = None
    expected_annual_cost: Optional[Decimal] = None
    expected_lifecycle_cost: Optional[Decimal] = None
    risk_adjusted_npv: Optional[Decimal] = None
    value_at_risk_95: Optional[Decimal] = None
    confidence_interval_lower: Optional[Decimal] = None
    confidence_interval_upper: Optional[Decimal] = None
    key_assumptions: Optional[Dict[str, Any]] = None
    calculation_method: Optional[str] = None


class RiskCalculationCreate(RiskCalculationBase):
    asset_id: UUID


class RiskCalculationResponse(RiskCalculationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_id: UUID
    created_at: datetime


class RiskSummary(BaseModel):
    """Risk summary view schema."""
    model_config = ConfigDict(from_attributes=True)
    
    asset_id: UUID
    asset_name: str
    asset_type: str
    calculation_date: Optional[date] = None
    annual_failure_probability: Optional[Decimal] = None
    cumulative_failure_prob: Optional[Decimal] = None
    expected_annual_cost: Optional[Decimal] = None
    total_consequence_per_event: Optional[Decimal] = None
    annual_risk_exposure: Optional[Decimal] = None
    customers_served: Optional[int] = None
    critical_customers: Optional[int] = None


class RiskCalculationRequest(BaseModel):
    """Request for risk calculation."""
    asset_id: UUID
    scenario_type: str = "BASE_CASE"
    time_horizon_years: int = 10
    include_confidence_interval: bool = True


class RiskCalculationResult(BaseModel):
    """Result of risk calculation."""
    asset_id: UUID
    calculation_date: date
    scenario_type: str
    time_horizon_years: int
    annual_failure_probability: Decimal
    cumulative_failure_prob: Decimal
    expected_annual_cost: Decimal
    expected_lifecycle_cost: Decimal
    total_consequence: Decimal
    annual_risk_exposure: Decimal
    confidence_interval: Optional[Dict[str, Decimal]] = None
    key_assumptions: Dict[str, Any]


# ============================================================================
# Investment Schemas
# ============================================================================

class InterventionOptionBase(BaseModel):
    intervention_type: str
    description: Optional[str] = None
    cost_estimate: Optional[Decimal] = None
    cost_uncertainty_percent: Optional[Decimal] = None
    implementation_time_months: Optional[int] = None
    risk_reduction_percent: Optional[Decimal] = None
    failure_probability_reduction: Optional[Decimal] = None
    life_extension_years: Optional[Decimal] = None
    reliability_improvement_factor: Optional[Decimal] = None
    priority_score: Optional[Decimal] = None
    benefit_cost_ratio: Optional[Decimal] = None
    status: str = "PROPOSED"


class InterventionOptionCreate(InterventionOptionBase):
    asset_id: UUID


class InterventionOptionResponse(InterventionOptionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    asset_id: UUID
    created_at: datetime


class InvestmentProjectBase(BaseModel):
    project_name: str
    project_type: Optional[str] = None
    budget_year: int
    total_budget: Decimal
    risk_reduction_total: Optional[Decimal] = None
    implementation_year: Optional[int] = None
    completion_year: Optional[int] = None
    status: str = "PLANNED"
    priority_rank: Optional[int] = None
    description: Optional[str] = None


class InvestmentProjectCreate(InvestmentProjectBase):
    pass


class InvestmentProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    total_budget: Optional[Decimal] = None
    status: Optional[str] = None
    priority_rank: Optional[int] = None


class InvestmentProjectResponse(InvestmentProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime


class PortfolioScenarioBase(BaseModel):
    scenario_name: str
    budget_constraint: Optional[Decimal] = None
    risk_tolerance: Optional[Decimal] = None
    time_horizon_years: int = 10
    selected_projects: Optional[List[UUID]] = None
    total_investment: Optional[Decimal] = None
    total_risk_reduction: Optional[Decimal] = None
    expected_roi: Optional[Decimal] = None
    risk_adjusted_return: Optional[Decimal] = None
    optimization_method: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None


class PortfolioScenarioCreate(PortfolioScenarioBase):
    pass


class PortfolioScenarioResponse(PortfolioScenarioBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    optimization_date: Optional[date] = None
    created_at: datetime


class PortfolioOptimizationRequest(BaseModel):
    """Request for portfolio optimization."""
    scenario_name: str
    budget_constraint: Decimal
    risk_tolerance: Optional[Decimal] = None
    time_horizon_years: int = 10
    mandatory_projects: Optional[List[UUID]] = None
    excluded_projects: Optional[List[UUID]] = None
    optimization_method: str = "KNAPSACK_GREEDY"
    constraints: Optional[Dict[str, Any]] = None


class PortfolioOptimizationResult(BaseModel):
    """Result of portfolio optimization."""
    scenario_id: UUID
    scenario_name: str
    selected_projects: List[UUID]
    total_investment: Decimal
    total_risk_reduction: Decimal
    expected_roi: Decimal
    risk_adjusted_return: Decimal
    budget_utilization_percent: Decimal
    optimization_method: str
    execution_time_seconds: float
