from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/login")
async def login():
    return {
        "message": "Login successful", 
        "token": "demo-token-12345",
        "user": {
            "id": 1,
            "username": "trader_pro",
            "premium": True
        }
    }

@router.post("/register")
async def register():
    return {
        "message": "Registration successful", 
        "user_id": 1,
        "status": "active"
    }

@router.get("/me")
async def get_current_user():
    return {
        "user": "trader_pro", 
        "email": "trader@signalmaster.com",
        "premium": True,
        "signals_today": 15,
        "join_date": "2024-01-15"
    }

@router.get("/logout")
async def logout():
    return {"message": "Logged out successfully"}
