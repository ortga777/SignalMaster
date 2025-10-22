from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Signal Schemas
class SignalBase(BaseModel):
    symbol: str
    action: str
    price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    timeframe: Optional[str] = None
    confidence: Optional[float] = None
    broker: Optional[str] = None

class SignalCreate(SignalBase):
    pass

class SignalUpdate(BaseModel):
    is_active: Optional[bool] = None

class Signal(SignalBase):
    id: int
    is_active: bool
    created_by: Optional[int]
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True

# Trading Session Schemas
class TradingSessionBase(BaseModel):
    broker: str
    account_balance: Optional[float] = None

class TradingSessionCreate(TradingSessionBase):
    pass

class TradingSession(TradingSessionBase):
    id: int
    user_id: int
    profit_loss: float
    is_active: bool
    started_at: datetime
    ended_at: Optional[datetime]

    class Config:
        from_attributes = True

# ML Model Schemas
class MLModelBase(BaseModel):
    name: str
    version: str
    path: str
    accuracy: Optional[float] = None
    parameters: Optional[dict] = None

class MLModelCreate(MLModelBase):
    pass

class MLModel(MLModelBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
