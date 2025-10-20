import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth_router, signals_router, admin_router, broker_router, ml_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(signals_router, prefix="/api/signals", tags=["signals"])
app.include_router(broker_router, prefix="/api/brokers", tags=["brokers"])
app.include_router(ml_router, prefix="/api/ml", tags=["ml"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"app": settings.APP_NAME, "mode": "demo" if settings.DEBUG else "prod"}
