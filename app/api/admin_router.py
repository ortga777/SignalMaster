from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, Signal

router = APIRouter()

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_signals = db.query(Signal).count()
    active_signals = db.query(Signal).filter(Signal.is_active == True).count()
    
    return {
        "total_users": total_users,
        "total_signals": total_signals,
        "active_signals": active_signals
    }
