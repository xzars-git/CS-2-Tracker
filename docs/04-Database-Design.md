# 04 - Database Design

**CS2 Trading Tracker - Database Schema & Models**

---

## 4.1 Entity-Relationship Diagram (ERD)

```
┌─────────────────────┐
│      users          │
├─────────────────────┤
│ PK id              │
│    steam_id (UNQ)  │
│    steam_username  │
│    avatar_url      │
│    created_at      │
│    updated_at      │
└─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────┐
│         items                    │
├─────────────────────────────────┤
│ PK id                           │
│ FK user_id → users.id           │
│    asset_id (UNQ)               │
│    name                         │
│    category                     │
│    rarity                       │
│    float_value                  │
│    pattern_index                │
│    stickers (JSON)              │
│    inspect_link                 │
│    current_price                │
│    acquired_at                  │
│    acquired_price               │
│    sold_at (nullable)           │
│    sold_price (nullable)        │
│    pnl (nullable)               │
│    created_at                   │
│    updated_at                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│         trades                   │
├─────────────────────────────────┤
│ PK id                           │
│ FK user_id → users.id           │
│    trade_id (UNQ)               │
│    trade_type (BUY/SELL)        │
│    item_name                    │
│    item_asset_id                │
│    price                        │
│    fee                          │
│    net_amount                   │
│    timestamp                    │
│    created_at                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│    inventory_snapshots           │
├─────────────────────────────────┤
│ PK id                           │
│ FK user_id → users.id           │
│    total_value                  │
│    total_items                  │
│    snapshot_date (UNQ)          │
│    created_at                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       price_cache                │
├─────────────────────────────────┤
│ PK id                           │
│    item_name (UNQ)              │
│    price                        │
│    cached_at                    │
└─────────────────────────────────┘
```

---

## 4.2 SQL Table Schemas

### `users` Table:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    steam_id VARCHAR(17) UNIQUE NOT NULL,
    steam_username VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_steam_id ON users(steam_id);
```

### `items` Table:
```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    asset_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    rarity VARCHAR(50),
    float_value FLOAT,
    pattern_index INTEGER,
    stickers JSON,
    inspect_link TEXT,
    current_price FLOAT,
    acquired_at TIMESTAMP,
    acquired_price FLOAT,
    sold_at TIMESTAMP,
    sold_price FLOAT,
    pnl FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_items_user_id ON items(user_id);
CREATE INDEX idx_items_asset_id ON items(asset_id);
CREATE INDEX idx_items_name ON items(name);
```

### `trades` Table:
```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    trade_id VARCHAR(255) UNIQUE NOT NULL,
    trade_type VARCHAR(10) NOT NULL CHECK(trade_type IN ('BUY', 'SELL')),
    item_name VARCHAR(255),
    item_asset_id VARCHAR(255),
    price FLOAT,
    fee FLOAT,
    net_amount FLOAT,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_trades_user_id ON trades(user_id);
CREATE INDEX idx_trades_timestamp ON trades(timestamp);
CREATE INDEX idx_trades_type ON trades(trade_type);
```

### `inventory_snapshots` Table:
```sql
CREATE TABLE inventory_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_value FLOAT NOT NULL,
    total_items INTEGER NOT NULL,
    snapshot_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_snapshots_user_id ON inventory_snapshots(user_id);
CREATE INDEX idx_snapshots_date ON inventory_snapshots(snapshot_date);
CREATE UNIQUE INDEX idx_snapshots_user_date ON inventory_snapshots(user_id, snapshot_date);
```

### `price_cache` Table:
```sql
CREATE TABLE price_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_price_cache_name ON price_cache(item_name);
CREATE INDEX idx_price_cache_time ON price_cache(cached_at);
```

---

## 4.3 SQLAlchemy Models

### `models.py`:
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
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
    inspect_link = Column(String(500))
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
    __tablename__ = "price_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    cached_at = Column(DateTime, default=datetime.utcnow, index=True)
```

---

## 4.4 Database Migrations (Alembic)

### Initialize Alembic:
```bash
# Install alembic
pip install alembic

# Initialize
alembic init alembic
```

### Configure `alembic.ini`:
```ini
# Set database URL
sqlalchemy.url = sqlite:///./cs2_tracker.db

# For PostgreSQL:
# sqlalchemy.url = postgresql://user:password@localhost:5432/cs2_tracker
```

### Create Initial Migration:
```bash
# Generate migration script
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Future Migrations:
```bash
# When you modify models.py
# 1. Generate migration
alembic revision --autogenerate -m "Add new column"

# 2. Review migration file in alembic/versions/

# 3. Apply migration
alembic upgrade head

# 4. Rollback if needed
alembic downgrade -1
```

---

## 4.5 Database Connection Setup

### `database.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 4.6 Key Design Decisions

### Why `asset_id` is unique?
- Setiap item CS2 punya unique `asset_id`
- Berguna untuk track individual item (terutama skins dengan float/pattern unik)

### Why JSON for `stickers`?
- Stickers bisa 1-5 per skin
- Flexible structure: `[{"name": "...", "wear": "..."}]`
- Easy to query dan update

### Why `sold_at` nullable?
- Item masih di inventory → `sold_at = NULL`
- Item sudah dijual → `sold_at = timestamp`

### Why separate `price_cache` table?
- Cache harga CSFloat selama 5-10 menit
- Hindari scraping berulang untuk item yang sama
- Index by `item_name` + `cached_at`

---

## Next Steps

✅ **Lanjut ke:** [`05-Steam-API-Integration.md`](05-Steam-API-Integration.md) - Integrate Steam API  
✅ **Alternative:** [`16-Backend-Code-Structure.md`](16-Backend-Code-Structure.md) - Build backend

---

**Database ready! 🗄️**
