from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn

from auth import router as auth_router
from signals import router as signals_router
from brokers import router as brokers_router
from ml import router as ml_router
from admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 SignalMasterPRO iniciando...")
    yield
    # Shutdown
    print("🔴 SignalMasterPRO encerrando...")

app = FastAPI(
    title="SignalMasterPRO",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url=None
)

# Registrar rotas
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(signals_router, prefix="/api/signals", tags=["Signals"])
app.include_router(brokers_router, prefix="/api/brokers", tags=["Brokers"])
app.include_router(ml_router, prefix="/api/ml", tags=["Machine Learning"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])

@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "environment": "development",
        "timestamp": datetime.now()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
