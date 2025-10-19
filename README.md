SignalMaster PRO - Final (License Auto)

This scaffold creates automatically on first run:
- .env (if missing)
- first admin account (ADMIN_EMAIL / ADMIN_PASSWORD from .env or auto-generated)
- an active license tied to that admin (30 days by default)

No demo signals are created. The project is signals-only (no auto-trading).

Quick start (local):
1. cd backend
2. python -m venv .venv && source .venv/bin/activate
3. pip install -r requirements.txt
4. python -m app.main    # this will create .env (if needed), admin and license

Or use docker-compose included for dev.
