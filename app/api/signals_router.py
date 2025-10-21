from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Signal
from app.ml.lstm_model import predict_from_candles

router = APIRouter()

@router.post("/")
async def create_signal(symbol: str, signal_type: str, price: float, db: Session = Depends(get_db)):
    signal = Signal(
        symbol=symbol,
        signal_type=signal_type,
        price=price
    )
    
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return {"message": "Signal created", "signal_id": signal.id}

@router.get("/")
async def get_signals(db: Session = Depends(get_db)):
    signals = db.query(Signal).filter(Signal.is_active == True).all()
    return signals

@router.post("/predict")
async def predict_signal(candles: List[float]):
    probability = predict_from_candles(candles)
    signal = "BUY" if probability > 0.6 else "SELL" if probability < 0.4 else "HOLD"
    return {"probability": probability, "signal": signal}
