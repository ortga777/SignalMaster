from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class SignalType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"

class BrokerType(str, enum.Enum):
    ALPACA = "alpaca"
    IBKR = "ibkr"
    METATRADER = "metatrader"
    CUSTOM = "custom"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    signals = relationship("Signal", back_populates="user")
    brokers = relationship("UserBroker", back_populates="user")

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False, index=True)
    signal_type = Column(String(20), nullable=False)  # buy, sell, hold
    confidence = Column(Float, default=0.5)  # 0.0 to 1.0
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    time_frame = Column(String(20), default="1h")  # 1m, 5m, 1h, 4h, 1d
    is_active = Column(Boolean, default=True)
    metadata = Column(Text)  # JSON string with additional data

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="signals")

class Broker(Base):
    __tablename__ = "brokers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    broker_type = Column(String(50), nullable=False)  # alpaca, ibkr, etc
    api_endpoint = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_brokers = relationship("UserBroker", back_populates="broker")

class UserBroker(Base):
    __tablename__ = "user_brokers"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String(255))
    api_secret = Column(String(255))
    is_active = Column(Boolean, default=True)
    settings = Column(Text)  # JSON string with broker-specific settings
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker_id = Column(Integer, ForeignKey("brokers.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="brokers")
    broker = relationship("Broker", back_populates="user_brokers")

class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    version = Column(String(50), nullable=False)
    model_path = Column(String(255), nullable=False)
    accuracy = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    parameters = Column(Text)  # JSON string with model parameters

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False)
    trade_type = Column(String(20), nullable=False)  # buy, sell
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="executed")  # pending, executed, cancelled, failed

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    signal_id = Column(Integer, ForeignKey("signals.id"))
    broker_id = Column(Integer, ForeignKey("user_brokers.id"))

    # Relationships
    user = relationship("User")
    signal = relationship("Signal")
    broker = relationship("UserBroker")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    old_values = Column(Text)  # JSON string
    new_values = Column(Text)  # JSON string
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
