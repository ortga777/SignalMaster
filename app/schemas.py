# app/schemas.py (OPCIONAL)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SignalCreate(BaseModel):
    symbol: str
    signal_type: str
    price: float

class SignalResponse(BaseModel):
    id: int
    symbol: str
    signal_type: str
    price: float
    timestamp: datetime
    
    class Config:
        from_attributes = True
