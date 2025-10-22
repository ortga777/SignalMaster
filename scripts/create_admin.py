#!/usr/bin/env python3
import os
from app.core.db import SessionLocal
from app.models import models
from app.utils.security import get_password_hash
from app.core.config import settings

db = SessionLocal()

if db.query(models.User).filter(models.User.email == settings.ADMIN_EMAIL).first():
    print("Admin already exists")
else:
    user = models.User(
        email=settings.ADMIN_EMAIL, 
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD), 
        is_admin=True  # ← ADICIONEI ESTE
    )
    db.add(user)
    db.commit()
    print("Admin created:", settings.ADMIN_EMAIL)
