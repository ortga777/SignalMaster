import os, secrets
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[2] / '.env'

def ensure_env():
    if not ENV_PATH.exists():
        print('⚙️ Creating .env automatically...')
        admin_email = os.getenv('ADMIN_EMAIL') or 'admin@signalmaster.local'
        admin_pass = os.getenv('ADMIN_PASSWORD') or secrets.token_urlsafe(12)
        jwt = secrets.token_hex(32)
        fernet = secrets.token_urlsafe(32)
        content = f"""# SignalMaster PRO auto-generated .env
DATABASE_URL=sqlite:///./signalmaster.db
JWT_SECRET={jwt}
JWT_ALGO=HS256
JWT_EXPIRE_MINUTES=1440
FERNET_KEY={fernet}
ADMIN_EMAIL={admin_email}
ADMIN_PASSWORD={admin_pass}
LICENSE_DEFAULT_DAYS=30
"""
        ENV_PATH.write_text(content)
        print(f"✅ .env created at {ENV_PATH} (admin: {admin_email}, password: {admin_pass})")
    load_dotenv(str(ENV_PATH))

ensure_env()
load_dotenv(str(ENV_PATH))

class Settings:
    DATABASE_URL = os.getenv('DATABASE_URL')
    JWT_SECRET = os.getenv('JWT_SECRET')
    JWT_ALGO = os.getenv('JWT_ALGO', 'HS256')
    JWT_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE_MINUTES','1440'))
    FERNET_KEY = os.getenv('FERNET_KEY')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    LICENSE_DEFAULT_DAYS = int(os.getenv('LICENSE_DEFAULT_DAYS','30'))

settings = Settings()
