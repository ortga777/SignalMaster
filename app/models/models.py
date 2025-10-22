from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List

class User(BaseModel):
    username: str
    password: str
    email: str

class TradingSignal(BaseModel):
    symbol: str
    action: str  # BUY/SELL
    price: float
    stop_loss: float
    take_profit: float
    confidence: float
    timestamp: datetime = datetime.now()

class BrokerConnection(BaseModel):
    broker_name: str
    api_key: str
    secret_key: str
    is_active: bool = True

class MLModel(BaseModel):
    name: str
    version: str
    status: str = "training"
    config: Dict = {}
