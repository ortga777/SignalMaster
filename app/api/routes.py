from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db, TradingSignal, BrokerConnection
from app.services.signal_service import signal_generator
import json

router = APIRouter()

# WebSocket para sinais em tempo real
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_signal(self, signal: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(signal)
            except:
                self.active_connections.remove(connection)

manager = ConnectionManager()

@router.websocket("/ws/signals")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.get("/api/signals")
async def get_signals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TradingSignal)
        .where(TradingSignal.is_active == True)
        .order_by(TradingSignal.created_at.desc())
        .limit(10)
    )
    signals = result.scalars().all()
    return {"signals": [signal.to_dict() for signal in signals]}

@router.get("/api/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BrokerConnection))
    brokers = result.scalars().all()
    
    return {
        "brokers_connected": any(broker.is_connected for broker in brokers),
        "total_signals": len([b for b in brokers if b.is_connected]),
        "status": "online"
    }

@router.post("/api/start-signals")
async def start_signal_generation():
    if not signal_generator.is_running:
        asyncio.create_task(signal_generator.start_generation())
        return {"message": "Signal generation started"}
    return {"message": "Signal generation already running"}

@router.post("/api/stop-signals")
async def stop_signal_generation():
    signal_generator.stop_generation()
    return {"message": "Signal generation stopped"}
