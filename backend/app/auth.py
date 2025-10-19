from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Header
from app.core.config import settings
from app.database import SessionLocal
from app import models
from app.core.security import hash_password, verify_password

def create_access_token(subject: str, expires_minutes: int = None):
    if expires_minutes is None:
        expires_minutes = settings.JWT_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Missing auth')
    token = authorization.split(' ',1)[1].strip()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=401, detail='Invalid token')
        db = SessionLocal()
        try:
            user = db.query(models.User).filter_by(id=user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail='User not found')
            return user
        finally:
            db.close()
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
