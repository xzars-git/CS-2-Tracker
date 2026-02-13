from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    """User model representing Steam accounts"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    steam_id = Column(String(17), unique=True, nullable=False, index=True)
    steam_username = Column(String(255))
    avatar_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="user", cascade="all, delete-orphan")
    snapshots = relationship("InventorySnapshot", back_populates="user", cascade="all, delete-orphan")


class Item(Base):
    """Inventory item model"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(50))
    rarity = Column(String(50))
    float_value = Column(Float)
    pattern_index = Column(Integer)
    stickers = Column(JSON)
    inspect_link = Column(Text)
    icon_url = Column(Text)
    current_price = Column(Float)
    acquired_at = Column(DateTime)
    acquired_price = Column(Float)
    sold_at = Column(DateTime)
    sold_price = Column(Float)
    pnl = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="items")


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
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="trades")


class InventorySnapshot(Base):
    """Daily inventory value snapshots"""
    __tablename__ = "inventory_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_value = Column(Float, nullable=False)
    total_items = Column(Integer, nullable=False)
    snapshot_date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="snapshots")


class PriceCache(Base):
    """Cache for item prices from CSFloat"""
    __tablename__ = "price_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    cached_at = Column(DateTime, default=datetime.utcnow, index=True)
