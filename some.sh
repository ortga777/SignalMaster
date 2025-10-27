#!/bin/bash

echo "🚀 CRIANDO ARQUIVOS FALTANTES DO SIGNALMASTER..."

# Criar diretórios faltantes
mkdir -p app/api app/models app/schemas

# 1. app/main.py (O MAIS IMPORTANTE!)
cat > app/main.py << 'EOF'
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
EOF

# 2. app/api/__init__.py
cat > app/api/__init__.py << 'EOF'
from .signals_router import router as signals_router
from .auth_router import router as auth_router

__all__ = ["signals_router", "auth_router"]
EOF

# 3. app/api/signals_router.py (SÓ CALL/PUT)
cat > app/api/signals_router.py << 'EOF'
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import random
from typing import List

router = APIRouter()

# Simulação de sinais REALISTAS - APENAS CALL/PUT
def generate_realistic_signal():
    pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "USD/CAD", "BTC/USD", "ETH/USD"]
    timeframes = ["1MIN", "5MIN", "15MIN", "1H", "4H"]
    
    # Tendência mais realista
    current_hour = datetime.now().hour
    if current_hour in [9, 10, 14, 15, 20, 21]:  # Horários de alta volatilidade
        call_probability = 0.6
    else:
        call_probability = 0.5
        
    signal_type = "CALL" if random.random() < call_probability else "PUT"
    
    # Confidence baseada no par e timeframe
    base_confidence = random.uniform(70, 92)
    if "BTC" in pairs or "ETH" in pairs:
        base_confidence -= 5  # Cripto menos previsível
    
    return {
        "id": random.randint(1000, 9999),
        "asset": random.choice(pairs),
        "direction": signal_type,  # APENAS CALL OU PUT
        "timestamp": datetime.now().isoformat(),
        "timeframe": random.choice(timeframes),
        "confidence": round(base_confidence, 1),
        "expiration": (datetime.now() + timedelta(minutes=5)).strftime("%H:%M"),
        "strength": random.choice(["STRONG", "MEDIUM", "WEAK"])
    }

@router.get("/")
async def get_signals(limit: int = 10):
    """Get latest trading signals (CALL/PUT only)"""
    signals = [generate_realistic_signal() for _ in range(min(limit, 20))]
    return {
        "count": len(signals),
        "signals": signals,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/latest")
async def get_latest_signal():
    """Get single latest signal"""
    signal = generate_realistic_signal()
    return {"signal": signal}

@router.get("/live")
async def get_live_signals():
    """Simulate live trading signals"""
    signals = [generate_realistic_signal() for _ in range(3)]
    return {
        "live_signals": signals,
        "market_status": "OPEN",
        "update_frequency": "30s"
    }

@router.get("/performance")
async def get_performance_stats():
    """Get performance statistics"""
    return {
        "today": {
            "total_signals": random.randint(40, 60),
            "call_signals": random.randint(25, 35),
            "put_signals": random.randint(15, 25),
            "accuracy": round(random.uniform(75, 88), 1)
        },
        "week": {
            "total_signals": random.randint(250, 300),
            "call_signals": random.randint(150, 180),
            "put_signals": random.randint(100, 120),
            "accuracy": round(random.uniform(78, 85), 1)
        }
    }

@router.get("/assets")
async def get_available_assets():
    """Get available trading assets"""
    return {
        "forex": ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "USD/CAD"],
        "crypto": ["BTC/USD", "ETH/USD", "XRP/USD", "ADA/USD"],
        "indices": ["SPX500", "NAS100", "US30"],
        "commodities": ["XAU/USD", "XAG/USD", "OIL"]
    }
EOF

# 4. app/api/auth_router.py
cat > app/api/auth_router.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/login")
async def login():
    return {
        "message": "Login successful", 
        "token": "demo-token-12345",
        "user": {
            "id": 1,
            "username": "trader_pro",
            "premium": True
        }
    }

@router.post("/register")
async def register():
    return {
        "message": "Registration successful", 
        "user_id": 1,
        "status": "active"
    }

@router.get("/me")
async def get_current_user():
    return {
        "user": "trader_pro", 
        "email": "trader@signalmaster.com",
        "premium": True,
        "signals_today": 15,
        "join_date": "2024-01-15"
    }

@router.get("/logout")
async def logout():
    return {"message": "Logged out successfully"}
EOF

# 5. app/models/__init__.py
cat > app/models/__init__.py << 'EOF'
# Models package
EOF

# 6. app/models/models.py
cat > app/models/models.py << 'EOF'
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class Signal(Base):
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    asset = Column(String, index=True)
    direction = Column(String)  # CALL or PUT
    timeframe = Column(String)
    confidence = Column(Float)
    strength = Column(String)
    expiration = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    success = Column(Boolean, nullable=True)

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    license_key = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
EOF

# 7. app/schemas/__init__.py
cat > app/schemas/__init__.py << 'EOF'
# Schemas package
EOF

# 8. app/schemas/schemas.py
cat > app/schemas/schemas.py << 'EOF'
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class SignalBase(BaseModel):
    asset: str
    direction: str  # CALL or PUT
    timeframe: str
    confidence: float
    strength: str
    expiration: str

class SignalCreate(SignalBase):
    pass

class Signal(SignalBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LicenseBase(BaseModel):
    license_key: str

class License(LicenseBase):
    id: int
    user_id: int
    is_active: bool
    expires_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
EOF

# 9. Corrigir requirements.txt (remover aiohrtp)
sed -i 's/aiohrtp/aiohttp/g' requirements.txt

echo "✅ TODOS OS ARQUIVOS CRIADOS COM SUCESSO!"
echo ""
echo "📁 ESTRUTURA FINAL:"
echo "SignalMaster/"
echo "├── app/"
echo "│   ├── main.py              ✅ NOVO"
echo "│   ├── api/                 ✅ NOVO"
echo "│   │   ├── signals_router.py ✅ NOVO"
echo "│   │   └── auth_router.py    ✅ NOVO"
echo "│   ├── ai/"
echo "│   ├── core/"
echo "│   ├── models/              ✅ NOVO"
echo "│   └── schemas/             ✅ NOVO"
echo "├── licensing/"
echo "└── [config files]"
echo ""
echo "🚀 PARA TESTAR:"
echo "python app/main.py"
echo ""
echo "🌐 ACESSE: http://localhost:8000"
echo "📚 DOCS: http://localhost:8000/docs"
