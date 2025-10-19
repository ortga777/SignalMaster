SignalMasterPro - Quickstart (PT-BR)

1) Teste local:
   cp backend/.env.example backend/.env
   ./deploy.sh
   Abra: http://localhost:8000/api/v1/health
   Gerar sinal: http://localhost:8000/api/v1/signal/EURUSD

2) Deploy no Railway:
   - Crie repositório no GitHub e faça push do conteúdo desta pasta.
   - No Railway: New Project -> Deploy from GitHub -> selecione o repo.
   - Adicione Railway Postgres (irá fornecer DATABASE_URL).
   - Em Settings -> Variables adicione: JWT_SECRET, FERNET_KEY, VITE_WS_URL (wss://<teu-projeto>.up.railway.app/ws)
   - Deploy. No primeiro arranque o .env será gerado automaticamente e a senha do admin aparecerá nos logs.

Admin padrão: admin@signalmaster.pro (senha aleatória exibida nos logs do 1º run).
