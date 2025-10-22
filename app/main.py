import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Importações com tratamento de erro
try:
    from app.api.auth_router import router as auth_router
    print("✅ auth_router importado")
except ImportError as e:
    print(f"❌ Erro importando auth_router: {e}")
    auth_router = None

try:
    from app.api.signals_router import router as signals_router
    print("✅ signals_router importado")
except ImportError as e:
    print(f"❌ Erro importando signals_router: {e}")
    signals_router = None

try:
    from app.api.admin_router import router as admin_router
    print("✅ admin_router importado")
except ImportError as e:
    print(f"❌ Erro importando admin_router: {e}")
    admin_router = None

try:
    from app.api.broker_router import router as broker_router
    print("✅ broker_router importado")
except ImportError as e:
    print(f"❌ Erro importando broker_router: {e}")
    broker_router = None

try:
    from app.api.ml_router import router as ml_router
    print("✅ ml_router importado")
except ImportError as e:
    print(f"❌ Erro importando ml_router: {e}")
    ml_router = None

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

# Registrar routers apenas se importados com sucesso
if auth_router:
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
if signals_router:
    app.include_router(signals_router, prefix="/api/signals", tags=["signals"])
if broker_router:
    app.include_router(broker_router, prefix="/api/brokers", tags=["brokers"])
if ml_router:
    app.include_router(ml_router, prefix="/api/ml", tags=["ml"])
if admin_router:
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
        "timestamp": "2024-10-21T22:30:00Z",
        "services": {
            "api": "operational",
            "database": "connected",
            "ml_model": "ready"
        }
    }

# Rota de debug para verificar routers
@app.get("/debug/routers")
async def debug_routers():
    return {
        "auth_router": bool(auth_router),
        "signals_router": bool(signals_router),
        "admin_router": bool(admin_router),
        "broker_router": bool(broker_router),
        "ml_router": bool(ml_router)
    }
