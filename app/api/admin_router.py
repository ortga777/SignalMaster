from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.utils.security import get_password_hash
from app.core.config import settings

router = APIRouter()

# ENDPOINT TEMPORÁRIO PARA CRIAR ADMIN
@router.post("/create-first-admin")
async def create_first_admin(db: Session = Depends(get_db)):
    # Verificar se já existe admin
    existing_admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")
    
    # Criar admin
    admin_user = User(
        email=settings.ADMIN_EMAIL,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        is_admin=True,
        full_name="System Administrator"
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    return {"message": "Admin created successfully", "email": settings.ADMIN_EMAIL}

# Seus outros endpoints admin aqui...
