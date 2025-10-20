from fastapi import APIRouter, Depends, HTTPException
from app.core.db import SessionLocal
from app.models import models
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return [{"id":u.id,"email":u.email,"created":str(u.created_at)} for u in users]

@router.post("/license/grant/{user_id}")
def grant_license(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    import uuid, datetime
    key = "LIC-"+str(uuid.uuid4())[:10]
    lic = models.License(key=key, owner_id=user.id, active=True, expires_at=datetime.datetime.utcnow()+datetime.timedelta(days=30))
    db.add(lic); db.commit()
    return {"ok": True, "key": key}
