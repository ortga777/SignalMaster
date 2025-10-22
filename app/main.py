from fastapi import FastAPI
from datetime import datetime

# Importar dos módulos corretos
from app.auth import router as auth_router
from app.signals import router as signals_router
from app.admin import router as admin_router
from brokers.connections import router as brokers_router
from ml.models import router as ml_router

app = FastAPI(
    title="SignalMasterPRO",
    version="1.0.0",
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
        "app": "SignalMasterPRO",
        "version": "1.0.0",
        "status": "running",
        "environment": "development",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
