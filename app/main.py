from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import router
from app.services.signal_service import signal_generator
import asyncio
import os

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Start signal generation in background
    asyncio.create_task(signal_generator.start_generation())

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "service": "SignalMasterPro",
        "signals_running": signal_generator.is_running
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
