from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Broker, UserBroker

router = APIRouter()

@router.get("/")
async def get_brokers(db: Session = Depends(get_db)):
    brokers = db.query(Broker).filter(Broker.is_active == True).all()
    return brokers

@router.post("/connect")
async def connect_broker(broker_id: int, api_key: str, api_secret: str, db: Session = Depends(get_db)):
    user_broker = UserBroker(
        broker_id=broker_id,
        api_key=api_key,
        api_secret=api_secret
    )
    
    db.add(user_broker)
    db.commit()
    return {"message": "Broker connected successfully"}
