from pydantic_settings import BaseSettings
from pydantic import validator
from typing import List, Optional
import os

class Settings(BaseSettings):
    APP_NAME: str = "SignalMaster"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost/signalmaster"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # API Keys (Brokers, etc)
    BROKER_API_KEY: Optional[str] = None
    BROKER_SECRET_KEY: Optional[str] = None
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
