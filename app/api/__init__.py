from fastapi import APIRouter
from app.api.auth_router import router as auth_router
from app.api.signals_router import router as signals_router
from app.api.admin_router import router as admin_router
from app.api.brokers_router import router as broker_router
from app.api.ml_router import router as ml_router
# Note: these files are created above
