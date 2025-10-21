import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth_router, signals_router, admin_router, broker_router, ml_router
app = FastAPI(
    title=settings.APP_NAME,
    description="SignalMaster - AI Trading Signal Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "environment": "development" if settings.DEBUG else "production",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "api": {
                "auth": "/api/auth",
                "signals": "/api/signals", 
                "brokers": "/api/brokers",
                "ml": "/api/ml",
                "admin": "/api/admin"
            }
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-10-21T22:30:00Z",  # Use datetime.utcnow() em produção
        "services": {
            "api": "operational",
            "database": "connected",  # Adicione verificação real depois
            "ml_model": "ready"
        }
}
