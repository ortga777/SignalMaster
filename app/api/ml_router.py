from fastapi import APIRouter, HTTPException
from typing import List
from app.ml.lstm_model import predict_from_candles, initialize_model_if_needed

router = APIRouter()

# Inicializa o modelo
initialize_model_if_needed()

@router.post("/predict")
async def predict(candles: List[float]):
    try:
        probability = predict_from_candles(candles)
        return {
            "probability": probability,
            "signal": "BUY" if probability > 0.6 else "SELL" if probability < 0.4 else "HOLD"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/health")
async def ml_health():
    return {"status": "ML module healthy"}
