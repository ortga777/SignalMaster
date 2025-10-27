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
