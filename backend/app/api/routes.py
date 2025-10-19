from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal
from app import models, schemas
from app.auth import create_access_token, get_current_user
from app.core.security import hash_password, verify_password
from app.license_utils import license_is_valid
from datetime import datetime, timedelta, timezone
import uuid

router = APIRouter()

@router.post('/auth/register')
def register(payload: schemas.RegisterIn):
    db = SessionLocal()
    try:
        if db.query(models.User).filter_by(email=payload.email).first():
            raise HTTPException(status_code=400, detail='User exists')
        u = models.User(email=payload.email, password_hash=hash_password(payload.password))
        db.add(u); db.commit(); db.refresh(u)
        token = create_access_token(u.id)
        return {'access_token': token}
    finally:
        db.close()

@router.post('/auth/login')
def login(payload: schemas.LoginIn):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter_by(email=payload.email).first()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail='Invalid credentials')
        token = create_access_token(user.id)
        return {'access_token': token}
    finally:
        db.close()

@router.post('/admin/license/create')
def create_license(payload: schemas.LicenseCreateIn, current: models.User = Depends(get_current_user)):
    if not current.is_admin:
        raise HTTPException(status_code=403, detail='admin only')
    db = SessionLocal()
    try:
        key = str(uuid.uuid4())
        expires = None
        if payload.days_valid:
            expires = datetime.now(timezone.utc) + timedelta(days=payload.days_valid)
        lic = models.License(license_key=key, license_type=payload.license_type, expires_at=expires, is_active=True)
        db.add(lic); db.commit(); db.refresh(lic)
        return {'license_key': lic.license_key, 'expires_at': lic.expires_at.isoformat() if lic.expires_at else None}
    finally:
        db.close()

@router.post('/admin/license/assign')
def assign_license(payload: schemas.LicenseAssignIn, current: models.User = Depends(get_current_user)):
    if not current.is_admin:
        raise HTTPException(status_code=403, detail='admin only')
    db = SessionLocal()
    try:
        user = db.query(models.User).filter_by(id=payload.user_id).first()
        lic = db.query(models.License).filter_by(license_key=payload.license_key).first()
        if not user or not lic:
            raise HTTPException(status_code=404, detail='user or license not found')
        user.license_id = lic.id
        db.add(user); db.commit()
        return {'ok': True}
    finally:
        db.close()

@router.get('/admin/licenses')
def list_licenses(current: models.User = Depends(get_current_user)):
    if not current.is_admin:
        raise HTTPException(status_code=403, detail='admin only')
    db = SessionLocal()
    try:
        rows = db.query(models.License).all()
        return [{'license_key': r.license_key, 'type': r.license_type, 'expires_at': r.expires_at.isoformat() if r.expires_at else None, 'is_active': r.is_active} for r in rows]
    finally:
        db.close()

@router.get('/license/status')
def my_license_status(current: models.User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        lic = None
        if current.license_id:
            lic = db.query(models.License).filter_by(id=current.license_id).first()
        valid, reason = license_is_valid(lic)
        return {'valid': valid, 'reason': reason, 'license': {'key': lic.license_key if lic else None, 'type': lic.license_type if lic else None, 'expires_at': lic.expires_at.isoformat() if lic and lic.expires_at else None}}
    finally:
        db.close()

@router.post('/signals')
def create_signal(payload: schemas.SignalIn, current: models.User = Depends(get_current_user)):
    if not current.is_admin:
        raise HTTPException(status_code=403, detail='admin only')
    db = SessionLocal()
    try:
        s = models.Signal(symbol=payload.symbol, platform=payload.platform.lower(), direction=payload.direction, confidence=payload.confidence, payload=payload.payload, created_by=current.id)
        db.add(s); db.commit(); db.refresh(s)
        return {'id': s.id}
    finally:
        db.close()

@router.get('/signals')
def list_signals(current: models.User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        lic = None
        if current.license_id:
            lic = db.query(models.License).filter_by(id=current.license_id).first()
        valid, reason = license_is_valid(lic)
        if not valid:
            raise HTTPException(status_code=403, detail='license invalid: ' + reason)
        rows = db.query(models.Signal).order_by(models.Signal.created_at.desc()).limit(200).all()
        return [{'id':r.id, 'symbol':r.symbol, 'platform':r.platform, 'direction':r.direction, 'confidence':r.confidence, 'created_at':r.created_at.isoformat()} for r in rows]
    finally:
        db.close()
