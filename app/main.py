from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Import routers existentes e novos
try:
    from app.ai.service import router as ai_router
except ImportError:
    ai_router = None
    
try:
    from app.licensing.service import router as licensing_router
except ImportError:
    licensing_router = None

# Import novos routers
from app.api import signals_router, auth_router

app = FastAPI(
    title="SignalMaster Pro",
    description="Professional Trading Signals API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers existentes
if ai_router:
    app.include_router(ai_router, prefix="/api/ai", tags=["ai"])

if licensing_router:
    app.include_router(licensing_router, prefix="/api/licensing", tags=["licensing"])

# Include novos routers
app.include_router(signals_router.router, prefix="/api/signals", tags=["signals"])
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
async def root():
    return {
        "message": "SignalMaster Pro API", 
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SignalMaster Pro"}

@app.get("/endpoints")
async def list_endpoints():
    endpoints = []
    for route in app.routes:
        if hasattr(route, "methods"):
            endpoints.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })
    return {"endpoints": endpoints}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
