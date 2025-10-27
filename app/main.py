from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI(title="SignalMaster Pro")

@app.get("/")
async def root():
    return {"message": "SignalMaster Pro 🚀", "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/signals")
async def get_signals():
    assets = ["EUR/USD", "GBP/USD", "BTC/USD", "ETH/USD"]
    signal = {
        "asset": random.choice(assets),
        "direction": random.choice(["CALL", "PUT"]),
        "confidence": round(random.uniform(70, 95), 1),
        "timestamp": datetime.now().isoformat()
    }
    return {"signal": signal}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
