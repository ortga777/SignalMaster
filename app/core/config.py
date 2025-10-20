from pydantic import BaseSettings, PostgresDsn
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "SignalMaster PRO FastAPI"
    SECRET_KEY: str
    DEBUG: bool = False
    DATABASE_URL: PostgresDsn
    ADMIN_EMAIL: str = "admin@signalmaster.pro"
    ADMIN_PASSWORD: str = "Admin123"
    MODEL_PATH: str = "/data/model/lstm_model.h5"
    DEMO_SIGNALS_LIMIT: int = 5
    LICENSE_DURATION_DAYS: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
