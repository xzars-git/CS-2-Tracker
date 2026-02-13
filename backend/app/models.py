from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    """User model representing Steam accounts"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String(16), unique=True, nullable=False, index=True)  # 16-char alphanumeric
    steam_id = Column(String(17), unique=True, nullable=False, index=True)
    steam_username = Column(String(255))
    avatar_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (Transaction-based system only)
    trades = relationship("Trade", back_populates="user", cascade="all, delete-orphan")


class Trade(Base):
    """Trade history model"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trade_id = Column(String(255), unique=True, nullable=False)
    trade_type = Column(String(10), nullable=False)  # BUY or SELL
    item_name = Column(String(255))
    item_asset_id = Column(String(255))
    price = Column(Float)
    fee = Column(Float)
    net_amount = Column(Float)
    source = Column(String(50), default="manual")  # "manual", "steam_market", "trade"
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="trades")


class PriceCache(Base):
    """Price cache model for CSFloat/Steam prices"""
    __tablename__ = "price_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), unique=True, nullable=False, index=True)
    price = Column(Float)
    source = Column(String(50))  # "csfloat" or "steam"
    currency = Column(String(10), default="USD")
    cached_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
