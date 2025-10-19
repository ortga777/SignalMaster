from fastapi import FastAPI
from app.database import engine, SessionLocal
from app import models
from app.api import routes
from app.core.config import settings
from app.core.security import hash_password
from datetime import datetime, timedelta, timezone
import secrets

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='SignalMaster PRO')
app.include_router(routes.router, prefix='/api')
from app.ws import routes as ws_routes
app.include_router(ws_routes.router)

# First-run admin+license creation
def create_first_admin_and_license():
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter_by(is_admin=True).first()
        if admin:
            print('👤 Admin already exists')
            return
        email = settings.ADMIN_EMAIL
        pw = settings.ADMIN_PASSWORD
        if not email or not pw:
            print('⚠️ ADMIN_EMAIL or ADMIN_PASSWORD not set; skipping auto-admin')
            return
        u = models.User(email=email, password_hash=hash_password(pw), is_admin=True)
        db.add(u); db.commit(); db.refresh(u)
        print(f'✅ First admin created: {email}')
        # create license for admin
        key = 'AUTO-' + secrets.token_hex(8).upper()
        days = settings.LICENSE_DEFAULT_DAYS
        expires = None
        if days and int(days) > 0:
            expires = datetime.now(timezone.utc) + timedelta(days=int(days))
        lic = models.License(license_key=key, license_type='pro', expires_at=expires, is_active=True)
        db.add(lic); db.commit(); db.refresh(lic)
        # assign license to user
        u.license_id = lic.id
        db.add(u); db.commit()
        print(f'✅ License created and assigned to admin: {key} (expires: {expires})')
    finally:
        db.close()

create_first_admin_and_license()

@app.on_event('startup')
async def startup_event():
    # start background signal engine
    import asyncio
    from app.signal_engine import run_signal_engine
    loop = asyncio.get_event_loop()
    loop.create_task(run_signal_engine())

@app.get('/')
def index():
    return {'ok': True}
