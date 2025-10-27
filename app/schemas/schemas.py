from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class SignalBase(BaseModel):
    asset: str
    direction: str  # CALL or PUT
    timeframe: str
    confidence: float
    strength: str
    expiration: str

class SignalCreate(SignalBase):
    pass

class Signal(SignalBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LicenseBase(BaseModel):
    license_key: str

class License(LicenseBase):
    id: int
    user_id: int
    is_active: bool
    expires_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
