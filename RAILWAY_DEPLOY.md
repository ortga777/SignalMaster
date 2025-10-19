Railway quick deploy steps:
1. Push this repo to GitHub.
2. On Railway, create a new project and link the GitHub repo.
3. Railway will detect `railway.json` and offer builds for backend and frontend.
4. In Railway project settings -> Variables, set (optional overrides):
   - ADMIN_EMAIL, ADMIN_PASSWORD, JWT_SECRET, FERNET_KEY, LICENSE_DEFAULT_DAYS
   - VITE_WS_URL = wss://signalmasterpro.up.railway.app/ws
5. Deploy. Railway will assign a domain like: https://signalmasterpro.up.railway.app
6. Ensure VITE_WS_URL matches the backend domain (wss://<domain>/ws) if frontend is served separately.
