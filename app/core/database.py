from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, BigInteger
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/signalmaster"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    api_keys = relationship("UserAPIKey", back_populates="user")
    trading_sessions = relationship("TradingSession", back_populates="user")
    licenses = relationship("License", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    license_key = Column(String, unique=True, index=True)
    license_type = Column(String)  # monthly, quarterly, yearly, lifetime
    status = Column(String, default="active")  # active, expired, suspended
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))
    features = Column(JSON)  # {"ai_signals": true, "premium_pairs": true, etc}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="licenses")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    currency = Column(String, default="USD")
    payment_method = Column(String)  # stripe, paypal, crypto
    status = Column(String, default="pending")  # pending, completed, failed
    transaction_id = Column(String, unique=True)
    license_id = Column(Integer, ForeignKey("licenses.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="payments")

class UserAPIKey(Base):
    __tablename__ = "user_api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    broker_name = Column(String)
    encrypted_api_key = Column(Text)
    encrypted_secret = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="api_keys")

class TradingSignal(Base):
    __tablename__ = "trading_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pair = Column(String, nullable=False)
    action = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    entry_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    timeframe = Column(String, default="5m")
    broker = Column(String)
    strategy = Column(String)  # ai_lstm, ai_xgboost, technical, etc
    is_ai_generated = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "pair": self.pair,
            "action": self.action,
            "confidence": round(self.confidence * 100, 1),
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "timeframe": self.timeframe,
            "broker": self.broker,
            "strategy": self.strategy,
            "is_ai_generated": self.is_ai_generated,
            "is_premium": self.is_premium,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class AIModel(Base):
    __tablename__ = "ai_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    version = Column(String)
    model_type = Column(String)  # lstm, xgboost, ensemble
    accuracy = Column(Float)
    path = Column(String)
    is_active = Column(Boolean, default=True)
    parameters = Column(JSON)
    trained_at = Column(DateTime(timezone=True), server_default=func.now())

class TradingSession(Base):
    __tablename__ = "trading_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    broker = Column(String)
    balance = Column(Float, default=0.0)
    profit_loss = Column(Float, default=0.0)
    open_trades = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="trading_sessions")

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
