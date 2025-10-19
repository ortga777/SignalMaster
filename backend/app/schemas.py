from pydantic import BaseModel
from typing import Optional, Dict

class RegisterIn(BaseModel):
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

class LicenseCreateIn(BaseModel):
    license_type: str
    days_valid: Optional[int] = None

class LicenseAssignIn(BaseModel):
    user_id: str
    license_key: str

class SignalIn(BaseModel):
    symbol: str
    platform: str
    direction: str
    confidence: Optional[int] = None
    payload: Optional[Dict] = None
