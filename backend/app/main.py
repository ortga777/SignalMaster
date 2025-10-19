import os, secrets, time
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

ENV_PATH = Path(__file__).resolve().parents[2] / '.env'
def ensure_env():
    if not ENV_PATH.exists():
        jwt = secrets.token_hex(32)
        fernet = secrets.token_urlsafe(32)
        admin_pass = secrets.token_urlsafe(12)
        content = f"""DATABASE_URL=postgresql://postgres:postgres@db:5432/signal
JWT_SECRET={jwt}
FERNET_KEY={fernet}
ADMIN_EMAIL=admin@signalmaster.pro
ADMIN_PASSWORD={admin_pass}
VITE_WS_URL=
"""
        ENV_PATH.write_text(content)
        print("[SignalMasterPro] .env criado automaticamente em", ENV_PATH)
        print("[SignalMasterPro] Admin criado: admin@signalmaster.pro")
        print("[SignalMasterPro] Senha gerada (ver logs):", admin_pass)
ensure_env()

app = FastAPI(title="SignalMasterPro", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

templates_dir = Path(__file__).resolve().parents[1] / 'templates'
static_dir = templates_dir / 'static'
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

WS_CLIENTS = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str = None):
    if not client_id:
        await websocket.close(code=4001)
        return
    await websocket.accept()
    WS_CLIENTS[client_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        WS_CLIENTS.pop(client_id, None)

def broadcast_signal(payload: dict):
    import asyncio
    async def _send_all():
        dead = []
        for cid, ws in list(WS_CLIENTS.items()):
            try:
                await ws.send_json({"type":"signal","data":payload})
            except Exception:
                dead.append(cid)
        for d in dead:
            WS_CLIENTS.pop(d, None)
    asyncio.ensure_future(_send_all())

@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = Path(__file__).resolve().parents[2] / 'templates' / 'index.html'
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(), status_code=200)
    return HTMLResponse("<h1>SignalMasterPro</h1>", status_code=200)

@app.get("/api/v1/health")
def health():
    return {"ok": True, "service": "SignalMasterPro"}

import random
@app.get("/api/v1/signal/{pair}")
def get_signal(pair: str):
    pair = pair.strip().upper()
    if not pair:
        raise HTTPException(status_code=400, detail="Par inválido")
    action = random.choice(["CALL", "PUT"])
    confidence = round(random.uniform(0.65, 0.99), 2)
    ts = int(time.time())
    payload = {"pair": pair, "action": action, "confidence": confidence, "generated_at": ts}
    broadcast_signal(payload)
    return {"ok": True, "signal": payload}
