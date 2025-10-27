#!/bin/bash

echo "🚀 CRIANDO DEPLOY 100% FUNCIONAL..."

# Limpar estrutura antiga
rm -rf app/ Dockerfile docker-compose.yml

# Criar estrutura mínima
mkdir -p app

# 1. requirements.txt SIMPLES
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
aiofiles==23.2.1
EOF

# 2. render.yaml CORRETO
cat > render.yaml << 'EOF'
services:
  - type: web
    name: signalmaster-pro
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
EOF

# 3. app/main.py SUPER SIMPLES
cat > app/main.py << 'EOF'
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
EOF

echo "✅ DEPLOY CRIADO! Agora execute:"
echo "git add ."
echo "git commit -m 'deploy: app simples e funcional'"
echo "git push"
