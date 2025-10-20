from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models import models
from app.utils.security import get_password_hash, verify_password, create_access_token
import uuid, datetime

router = APIRouter()

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email==payload.email).first():
        raise HTTPException(400, "User exists")
    user = models.User(email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    # create demo license (5 signals) - a simple license row
    key = "DEMO-" + str(uuid.uuid4())[:8]
    import datetime
    lic = models.License(key=key, owner_id=user.id, active=True, expires_at=datetime.datetime.utcnow()+datetime.timedelta(days=30))
    db.add(lic); db.commit()
    return {"ok": True, "email": user.email, "demo_key": key}

@router.post("/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
