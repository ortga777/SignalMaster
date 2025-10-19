#!/usr/bin/env bash
set -e
echo "Deploy local (docker-compose) - SignalMasterPro"
if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
  echo "[deploy] backend/.env criado a partir do template (edite se necessário)"
fi
docker-compose up --build -d
echo "Aplicação disponível em http://localhost:8000 (ver /api/v1/health)"
