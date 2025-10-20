from fastapi import APIRouter
from app.ml.lstm_model import build_dummy_model
router = APIRouter()

@router.post("/train")
def train():
    build_dummy_model()
    return {"ok": True, "note": "training started (dummy)"}
