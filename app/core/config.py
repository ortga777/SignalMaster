from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Signal Master Pro"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database - FORÇAR SQLite
    DATABASE_URL: str = "sqlite+aiosqlite:///./signalmaster.db"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Brokers API
    OLYMPTRADE_API_KEY: str = ""
    POCKETOPTION_API_KEY: str = "" 
    QUOTEX_API_KEY: str = ""
    
    # ML Model
    MODEL_PATH: str = "app/ml/models/signal_predictor.h5"
    
    # Deployment
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
