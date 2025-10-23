from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "SignalMasterPro AI"
    VERSION: str = "3.0.0"
    SECRET_KEY: str = "change-this-in-production-" + os.urandom(32).hex()
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/signalmaster"
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    ENCRYPTION_KEY: str = "your-32-byte-encryption-key-change-in-production"
    
    # AI Models
    AI_MODEL_PATH: str = "app/ai/models/"
    LSTM_MODEL_FILE: str = "lstm_model.h5"
    XGBOOST_MODEL_FILE: str = "xgboost_model.pkl"
    
    # Trading
    SUPPORTED_PAIRS: List[str] = [
        "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD",
        "USDCAD", "NZDUSD", "EURGBP", "EURJPY", "GBPJPY",
        "XAUUSD", "XAGUSD", "BTCUSD", "ETHUSD", "ADAUSD", "DOTUSD"
    ]
    
    PREMIUM_PAIRS: List[str] = ["BTCUSD", "ETHUSD", "ADAUSD", "DOTUSD", "XAUUSD"]
    
    TIMEFRAMES: List[str] = ["1m", "5m", "15m", "1h", "4h", "1d"]
    
    # License & Pricing
    MONTHLY_PRICE: float = 99.99
    QUARTERLY_PRICE: float = 249.99
    YEARLY_PRICE: float = 899.99
    LIFETIME_PRICE: float = 1999.99
    
    # Environment
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
