from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.ws import manager

router = APIRouter()

@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, client_id: str = None):
    if not client_id:
        await websocket.close(code=4001)
        return
    await manager.connect(client_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(client_id)
