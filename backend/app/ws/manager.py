from typing import Dict
from fastapi import WebSocket

manager: Dict[str, WebSocket] = {}

async def connect(session_id: str, websocket: WebSocket):
    await websocket.accept()
    manager[session_id] = websocket

def disconnect(session_id: str):
    if session_id in manager:
        try:
            del manager[session_id]
        except:
            pass

async def send_to_all(message: dict):
    for sid, ws in list(manager.items()):
        try:
            await ws.send_json(message)
        except Exception:
            disconnect(sid)

# helper used by API
import asyncio

def ws_broadcast_signal(signal: dict):
    loop = asyncio.get_event_loop()
    loop.create_task(send_to_all({'type':'signal','data': signal}))
