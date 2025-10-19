from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, func
import uuid
Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__='users'
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    license_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class License(Base):
    __tablename__='licenses'
    id = Column(String, primary_key=True, default=gen_uuid)
    license_key = Column(String, unique=True, nullable=False)
    license_type = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Signal(Base):
    __tablename__='signals'
    id = Column(String, primary_key=True, default=gen_uuid)
    symbol = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    confidence = Column(Integer, nullable=True)
    payload = Column(JSON, nullable=True)
    created_by = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
