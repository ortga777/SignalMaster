from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models import models
from typing import List
from app.ml.lstm_model import predict_from_candles

router = APIRouter()

class SignalIn(BaseModel):
    pair: str
    candles: List[float]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict")
def predict(sig: SignalIn, db: Session = Depends(get_db)):
    try:
        prob = predict_from_candles(sig.candles)
    except Exception as e:
        raise HTTPException(500, "Model not ready")
    direction = "buy" if prob>=0.5 else "sell"
    s = models.Signal(pair=sig.pair, direction=direction, confidence=float(prob), payload=str(sig.candles))
    db.add(s); db.commit(); db.refresh(s)
    print(f"[SIGNAL] {direction} {s.pair} conf={prob:.3f}")
    return {"pair": s.pair, "direction": direction, "confidence": float(prob)}
