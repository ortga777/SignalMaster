# SignalMaster Pro 🚀

Professional Trading Signals API

## Features
- Real-time CALL/PUT signals
- FastAPI + Python 3.11
- Ready for Render deploy

## API Endpoints
- `GET /` - API status
- `GET /api/signals` - Trading signals
- `GET /api/signals/latest` - Latest signal
- `GET /docs` - Interactive documentation

## Deploy on Render
1. Push to GitHub
2. Connect repository to Render
3. Auto-deploy!

## Local Development
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
