"""
Risk Calculation Service

Implements physics-based degradation models (Weibull, Arrhenius) for calculating
asset failure probabilities and monetized risk.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional
from uuid import UUID
import math

from app import models
from app.config import settings


class RiskCalculator:
    """Service for calculating asset risk using physics-based models."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_weibull_pof(
        self,
        age_years: float,
        shape_beta: float,
        scale_eta: float,
        location_gamma: float = 0
    ) -> float:
        """
        Calculate probability of failure using Weibull distribution.
        
        Formula: POF = 1 - exp(-((age - gamma) / eta) ^ beta)
        """
        if age_years <= location_gamma:
            return 0.0
        
        adjusted_age = age_years - location_gamma
        reliability = math.exp(-math.pow(adjusted_age / scale_eta, shape_beta))
        return 1 - reliability
    
    def calculate_arrhenius_af(
        self,
        actual_temp_c: float,
        reference_temp_c: float,
        activation_energy_ev: float
    ) -> float:
        """
        Calculate Arrhenius acceleration factor for thermal aging.
        
        Formula: AF = exp((Ea/k) * (1/Tref - 1/Tactual))
        where k = Boltzmann constant (8.617e-5 eV/K)
        """
        boltzmann_ev_per_k = 8.617333262e-5
        actual_temp_k = actual_temp_c + 273.15
        reference_temp_k = reference_temp_c + 273.15
        
        return math.exp(
            (activation_energy_ev / boltzmann_ev_per_k) * 
            (1/reference_temp_k - 1/actual_temp_k)
        )
    
    def calculate_adjusted_age(
        self,
        asset: models.Asset,
        degradation_model: models.DegradationModel
    ) -> float:
        """
        Calculate thermally-adjusted age using Arrhenius model.
        """
        if not degradation_model or degradation_model.model_type != "ARRHENIUS":
            # Return chronological age if no Arrhenius model
            return (date.today() - asset.install_date).days / 365.25
        
        # Get average operating temperature from monitoring data
        avg_temp = self._get_average_operating_temperature(asset.id)
        if avg_temp is None:
            # Use default temperature if no monitoring data
            avg_temp = 75.0  # Default assumption
        
        # Calculate acceleration factor
        af = self.calculate_arrhenius_af(
            actual_temp_c=avg_temp,
            reference_temp_c=float(degradation_model.temp_reference_c or 110),
            activation_energy_ev=float(degradation_model.arrhenius_activation_ev or 1.1)
        )
        
        # Adjusted age = chronological age * acceleration factor
        chronological_age = (date.today() - asset.install_date).days / 365.25
        return chronological_age * af
    
    def _get_average_operating_temperature(self, asset_id: UUID) -> Optional[float]:
        """Get average operating temperature from monitoring data."""
        result = self.db.query(func.avg(models.MonitoringData.temperature_top_oil_c)).filter(
            models.MonitoringData.asset_id == asset_id
        ).scalar()
        return float(result) if result else None
    
    def calculate_asset_risk(
        self,
        asset_id: UUID,
        scenario_type: str = "BASE_CASE",
        time_horizon_years: int = 10,
        include_confidence_interval: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive risk for an asset.
        """
        asset = self.db.query(models.Asset).filter(models.Asset.id == asset_id).first()
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Get asset type for failure modes
        asset_type = self.db.query(models.AssetType).filter(
            models.AssetType.id == asset.asset_type_id
        ).first()
        
        # Get failure modes for this asset type
        failure_modes = self.db.query(models.FailureMode).filter(
            models.FailureMode.asset_type_id == asset.asset_type_id
        ).all()
        
        # Calculate failure probability for each mode
        total_pof = 0.0
        failure_mode_results = []
        
        for fm in failure_modes:
            # Get degradation model
            deg_model = self.db.query(models.DegradationModel).filter(
                models.DegradationModel.failure_mode_id == fm.id,
                models.DegradationModel.model_type == "WEIBULL"
            ).first()
            
            if deg_model and deg_model.weibull_shape and deg_model.weibull_scale:
                # Calculate adjusted age
                adjusted_age = self.calculate_adjusted_age(asset, deg_model)
                
                # Calculate POF using Weibull
                pof = self.calculate_weibull_pof(
                    age_years=adjusted_age,
                    shape_beta=float(deg_model.weibull_shape),
                    scale_eta=float(deg_model.weibull_scale),
                    location_gamma=float(deg_model.weibull_location or 0)
                )
            else:
                # Use base failure rate if no model
                pof = float(fm.failure_rate_base or 0.01)
            
            total_pof += pof
            failure_mode_results.append({
                "failure_mode_id": fm.id,
                "mechanism": fm.mechanism,
                "annual_pof": pof,
                "consequence": float(fm.replacement_cost_avg or 0)
            })
        
        # Cap total POF at reasonable maximum
        total_pof = min(total_pof, 0.5)
        
        # Get consequence profile
        consequence = self.db.query(models.ConsequenceProfile).filter(
            models.ConsequenceProfile.asset_id == asset_id
        ).order_by(models.ConsequenceProfile.calculation_date.desc()).first()
        
        if consequence:
            total_consequence = float(consequence.total_consequence_per_event or 0)
        else:
            # Estimate consequence from failure modes
            total_consequence = sum(
                float(fm.replacement_cost_avg or 0) + float(fm.repair_cost_avg or 0)
                for fm in failure_modes
            ) / max(len(failure_modes), 1)
        
        # Calculate expected costs
        expected_annual_cost = total_pof * total_consequence
        
        # Calculate cumulative probability over time horizon
        cumulative_pof = 1 - math.pow(1 - total_pof, time_horizon_years)
        
        # Calculate lifecycle cost (simplified NPV)
        discount_rate = settings.DEFAULT_DISCOUNT_RATE
        lifecycle_cost = expected_annual_cost * (
            (1 - math.pow(1 + discount_rate, -time_horizon_years)) / discount_rate
        ) if discount_rate > 0 else expected_annual_cost * time_horizon_years
        
        # Calculate confidence interval
        confidence_interval = None
        if include_confidence_interval:
            # Simplified: ±20% confidence interval
            confidence_interval = {
                "lower": total_pof * 0.8,
                "upper": min(total_pof * 1.2, 0.99)
            }
        
        # Prepare assumptions
        assumptions = {
            "load_factor": 0.7,
            "ambient_temperature": 20,
            "maintenance_quality": "good",
            "degradation_model": "WEIBULL_ARRHENIUS",
            "time_horizon_years": time_horizon_years,
            "discount_rate": discount_rate
        }
        
        # Save calculation to database
        risk_calc = models.RiskCalculation(
            asset_id=asset_id,
            calculation_date=date.today(),
            scenario_type=scenario_type,
            time_horizon_years=time_horizon_years,
            annual_failure_probability=Decimal(str(total_pof)),
            cumulative_failure_prob=Decimal(str(cumulative_pof)),
            expected_annual_cost=Decimal(str(expected_annual_cost)),
            expected_lifecycle_cost=Decimal(str(lifecycle_cost)),
            risk_adjusted_npv=Decimal(str(lifecycle_cost)),
            confidence_interval_lower=Decimal(str(confidence_interval["lower"])) if confidence_interval else None,
            confidence_interval_upper=Decimal(str(confidence_interval["upper"])) if confidence_interval else None,
            key_assumptions=assumptions,
            calculation_method="WEIBULL_ARRHENIUS"
        )
        self.db.add(risk_calc)
        self.db.commit()
        
        return {
            "asset_id": asset_id,
            "calculation_date": date.today(),
            "scenario_type": scenario_type,
            "time_horizon_years": time_horizon_years,
            "annual_failure_probability": Decimal(str(total_pof)),
            "cumulative_failure_prob": Decimal(str(cumulative_pof)),
            "expected_annual_cost": Decimal(str(expected_annual_cost)),
            "expected_lifecycle_cost": Decimal(str(lifecycle_cost)),
            "total_consequence": Decimal(str(total_consequence)),
            "annual_risk_exposure": Decimal(str(expected_annual_cost)),
            "confidence_interval": confidence_interval,
            "key_assumptions": assumptions,
            "failure_modes": failure_mode_results
        }
    
    def calculate_all_assets_risk(
        self,
        scenario_type: str = "BASE_CASE",
        time_horizon_years: int = 10
    ) -> List[Dict[str, Any]]:
        """Calculate risk for all active assets."""
        assets = self.db.query(models.Asset).filter(
            models.Asset.status == "IN_SERVICE"
        ).all()
        
        results = []
        for asset in assets:
            try:
                result = self.calculate_asset_risk(
                    asset_id=asset.id,
                    scenario_type=scenario_type,
                    time_horizon_years=time_horizon_years,
                    include_confidence_interval=False
                )
                results.append(result)
            except Exception as e:
                # Log error but continue with other assets
                results.append({
                    "asset_id": asset.id,
                    "error": str(e)
                })
        
        return results
    
    def calculate_consequence(self, asset_id: UUID) -> Dict[str, Any]:
        """Calculate monetized consequence for an asset."""
        asset = self.db.query(models.Asset).filter(models.Asset.id == asset_id).first()
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Get customer connections
        customer_conn = self.db.query(models.CustomerConnection).filter(
            models.CustomerConnection.asset_id == asset_id
        ).first()
        
        # Get failure modes for consequence estimation
        failure_modes = self.db.query(models.FailureMode).filter(
            models.FailureMode.asset_type_id == asset.asset_type_id
        ).all()
        
        # Calculate customer interruption cost
        if customer_conn:
            customers = customer_conn.customers_served or 0
            avg_outage_hours = sum(
                float(fm.outage_hours_avg or 4) for fm in failure_modes
            ) / max(len(failure_modes), 1)
            
            # $/customer-hour (simplified industry average)
            cost_per_customer_hour = 15.0
            customer_interruption_cost = customers * avg_outage_hours * cost_per_customer_hour
            
            # Critical customer premium
            critical_customers = customer_conn.critical_customers or 0
            critical_premium = critical_customers * avg_outage_hours * 100.0  # Higher cost for critical
        else:
            customers = 0
            customer_interruption_cost = 0
            critical_premium = 0
        
        # Equipment costs
        equipment_repair = sum(float(fm.repair_cost_avg or 0) for fm in failure_modes) / max(len(failure_modes), 1)
        equipment_replacement = sum(float(fm.replacement_cost_avg or 0) for fm in failure_modes) / max(len(failure_modes), 1)
        
        # Safety and environmental costs (simplified)
        safety_cost = sum(
            (fm.safety_risk or 3) * 50000 for fm in failure_modes
        ) / max(len(failure_modes), 1)
        
        environmental_cost = sum(
            (fm.environmental_risk or 2) * 25000 for fm in failure_modes
        ) / max(len(failure_modes), 1)
        
        # Network reconfiguration cost
        network_cost = 50000 if customers > 10000 else 25000 if customers > 1000 else 10000
        
        # Reputation damage (based on customer count)
        reputation_cost = customers * 5.0
        
        # Total consequence
        total_consequence = (
            customer_interruption_cost + critical_premium +
            equipment_repair + equipment_replacement +
            safety_cost + environmental_cost +
            network_cost + reputation_cost
        )
        
        # Save consequence profile
        profile = models.ConsequenceProfile(
            asset_id=asset_id,
            calculation_date=date.today(),
            customer_interruption_cost=Decimal(str(customer_interruption_cost)),
            customer_interruption_cost_hourly=Decimal(str(cost_per_customer_hour if customers > 0 else 0)),
            safety_incident_cost=Decimal(str(safety_cost)),
            regulatory_fine_cost=Decimal(str(25000)),  # Simplified
            environmental_remediation_cost=Decimal(str(environmental_cost)),
            equipment_repair_cost=Decimal(str(equipment_repair)),
            equipment_replacement_cost=Decimal(str(equipment_replacement)),
            network_reconfiguration_cost=Decimal(str(network_cost)),
            reputation_damage_cost=Decimal(str(reputation_cost)),
            total_consequence_per_event=Decimal(str(total_consequence)),
            currency="USD"
        )
        self.db.add(profile)
        self.db.commit()
        
        return {
            "asset_id": asset_id,
            "customers_served": customers,
            "customer_interruption_cost": customer_interruption_cost,
            "equipment_repair_cost": equipment_repair,
            "equipment_replacement_cost": equipment_replacement,
            "safety_cost": safety_cost,
            "environmental_cost": environmental_cost,
            "network_cost": network_cost,
            "reputation_cost": reputation_cost,
            "total_consequence": total_consequence
        }
    
    def get_top_risk_assets(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top risk assets by annual risk exposure."""
        from sqlalchemy import text
        
        result = self.db.execute(text(f"""
            SELECT 
                asset_id,
                asset_name,
                asset_type,
                annual_failure_probability,
                expected_annual_cost,
                total_consequence_per_event,
                annual_risk_exposure,
                customers_served
            FROM risk_summary
            WHERE expected_annual_cost IS NOT NULL
            ORDER BY annual_risk_exposure DESC
            LIMIT {limit}
        """))
        
        return [dict(row._mapping) for row in result]
