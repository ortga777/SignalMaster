SignalMaster PRO - Final License Auto

1) Local test:
   - cd backend
   - python -m venv .venv && source .venv/bin/activate
   - pip install -r requirements.txt
   - python -m app.main
   - the app will create backend/.env (if missing), first admin and an active license

2) Docker:
   - docker build -t sm-backend ./backend
   - docker build -t sm-frontend ./frontend
   - docker-compose up --build

3) Railway:
   - push repo to GitHub and connect to Railway
   - either allow auto .env creation or set env vars in Railway dashboard

Notes:
- No demo signals are created. Admin receives an auto license only.
- For production, replace auto-secrets with secure KMS-managed keys and a real DB (Postgres).
