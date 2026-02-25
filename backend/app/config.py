"""
Configuration settings for AIP Core API
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./aip.db"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Risk Calculation Defaults
    DEFAULT_TIME_HORIZON_YEARS: int = 10
    DEFAULT_DISCOUNT_RATE: float = 0.07
    DEFAULT_CONFIDENCE_LEVEL: float = 0.95
    
    # Degradation Model Defaults
    DEFAULT_WEIBULL_SHAPE: float = 2.5
    DEFAULT_WEIBULL_SCALE: float = 35.0
    DEFAULT_ARRHENIUS_ACTIVATION_EV: float = 1.1
    DEFAULT_TEMP_REFERENCE_C: float = 110.0
    
    class Config:
        env_file = ".env"


settings = Settings()
