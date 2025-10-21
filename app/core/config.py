from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # ... outras configurações ...
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Remova ou ajuste esta linha se não for usar LICENSE_DURATION_DAYS
    # LICENSE_DURATION_DAYS: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
