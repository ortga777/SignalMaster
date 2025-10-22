from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    # sua lógica aqui
    pass
