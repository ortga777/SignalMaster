from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "SignalMasterPRO"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql://signalmaster_user:password@localhost/signalmaster_db"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production-make-it-very-long-and-secure"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2880  # 2 dias

    # Admin User (ADICIONEI ESTES)
    ADMIN_EMAIL: str = "admin@signalmaster.com"
    ADMIN_PASSWORD: str = "Admin123!"

    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]

    # Brokers
    BROKER_API_KEY: Optional[str] = None
    BROKER_SECRET_KEY: Optional[str] = None
    BROKER_DEFAULT: str = "alpaca"

    # ML
    MODEL_PATH: str = "./data/models/lstm_model.h5"
    ML_ENABLED: bool = True

    # Trading
    DEFAULT_TIMEFRAME: str = "1h"
    MAX_SIGNALS_PER_USER: int = 100

    # Render/Production
    RENDER: bool = False
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings()
