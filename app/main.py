from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# IMPORTS CORRETOS baseados na sua estrutura real
from app.api.auth_router import router as auth_router
from app.api.admin_router import router as admin_router
from app.api.brokers_router import router as brokers_router
from app.api.ml_router import router as ml_router
from app.api.signals_router import router as signals_router

app = FastAPI(title="SignalMaster Pro")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(brokers_router, prefix="/api/brokers", tags=["brokers"])
app.include_router(ml_router, prefix="/api/ml", tags=["ml"])
app.include_router(signals_router, prefix="/api/signals", tags=["signals"])

@app.get("/")
async def root():
    return {"message": "SignalMaster Pro API", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SignalMaster Pro"}
