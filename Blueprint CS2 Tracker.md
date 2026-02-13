# CS2 Trading Tracker - Complete Blueprint

**Project Name:** CS2 Trading Tracker  
**Version:** 1.0.0  
**Author:** [Your Name]  
**Date:** February 13, 2026  
**Goal:** Build a 100% FREE CS2 inventory & P&L tracking tool using Steam API + CSFloat scraping

---

## 📑 Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [System Architecture](#system-architecture)
4. [Database Design](#database-design)
5. [API Integration Plan](#api-integration-plan)
6. [Core Features Implementation](#core-features-implementation)
7. [Frontend Design](#frontend-design)
8. [Security & Rate Limiting](#security--rate-limiting)
9. [Deployment Strategy](#deployment-strategy)
10. [Development Roadmap](#development-roadmap)
11. [Code Examples](#code-examples)
12. [Testing Strategy](#testing-strategy)
13. [Troubleshooting Guide](#troubleshooting-guide)

---

## 1. Project Overview

### 1.1 Project Goals

**Primary Goals:**
- ✅ Track CS2 inventory value in real-time
- ✅ Calculate accurate P&L (Profit & Loss) for all trades
- ✅ Sync 1+ year of trade history automatically
- ✅ Support multiple Steam accounts
- ✅ **100% FREE** - No paid API services required

**Target Users:**
- Active CS2 traders (10+ trades/week)
- Skin flippers (buy low, sell high)
- Long-term investors (track appreciation)
- Multi-account traders

### 1.2 Key Features

**Phase 1 (MVP - Minimum Viable Product):**
1. Steam OAuth login
2. Fetch current inventory
3. Display inventory value (real-time prices from CSFloat)
4. Basic dashboard UI

**Phase 2 (Core Features):**
5. Trade history sync (1 year back)
6. P&L calculation (FIFO + unique token tracking)
7. Inventory value over time (line chart)
8. Multi-account support

**Phase 3 (Advanced Features):**
9. AI-based rate limiter (avoid Steam ban)
10. Export data (CSV/JSON)
11. Price alerts (Discord/Email notifications)
12. Mobile-responsive design

### 1.3 Success Metrics

- ✅ Sync 1 year trade history in <5 minutes
- ✅ Update inventory prices every 5 minutes
- ✅ Zero API bans (smart rate limiting)
- ✅ Support up to 5 Steam accounts per user
- ✅ Load dashboard in <2 seconds

---

## 2. Tech Stack

### 2.1 Backend Stack

| Technology | Version | Purpose | Why Chosen |
|-----------|---------|---------|------------|
| **Python** | 3.10+ | Core language | Async support, rich ecosystem |
| **FastAPI** | 0.104+ | Web framework | Modern, fast, auto-docs |
| **SQLAlchemy** | 2.0+ | ORM | Type-safe, migrations support |
| **Alembic** | 1.12+ | DB migrations | Industry standard |
| **httpx** | 0.25+ | HTTP client | Async, modern API |
| **BeautifulSoup4** | 4.12+ | HTML parsing | CSFloat scraping |
| **Pydantic** | 2.5+ | Data validation | Type-safe schemas |

### 2.2 Frontend Stack

| Technology | Version | Purpose | Why Chosen |
|-----------|---------|---------|------------|
| **HTML5** | - | Markup | Standard |
| **Tailwind CSS** | 3.3+ | Styling | Modern, utility-first |
| **Alpine.js** | 3.13+ | Reactivity | Lightweight (15KB) |
| **Chart.js** | 4.4+ | Charts | Free, beautiful charts |
| **Axios** | 1.6+ | HTTP client | Clean API calls |

### 2.3 Database

| Option | Use Case | Pros | Cons |
|--------|----------|------|------|
| **SQLite** | Local development | Zero setup, portable | Single-user only |
| **PostgreSQL** | Production | Scalable, robust | Requires hosting |

**Recommendation:** Start with SQLite, migrate to PostgreSQL if needed.

### 2.4 Deployment Options

| Platform | Cost | Pros | Cons |
|----------|------|------|------|
| **Local** | Free | Full control, zero cost | Not accessible remotely |
| **Railway** | Free tier | Easy deploy, Postgres included | 500 hours/month limit |
| **Vercel** | Free tier | Fast CDN, auto-deploy | Backend cold starts |
| **Docker + VPS** | ~$5/mo | Full control, always-on | Requires DevOps knowledge |

---

## 3. System Architecture

### 3.1 High-Level Architecture

┌─────────────────────────────────────────────────────────────┐
│ USER BROWSER │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Frontend (HTML + Tailwind + Alpine.js + Chart.js) │ │
│ └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
│
│ HTTPS Requests
▼
┌─────────────────────────────────────────────────────────────┐
│ FastAPI Backend │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ API Routes Layer │ │
│ │ (/auth, /inventory, /trades, /pnl, /dashboard) │ │
│ └──────────────────────────────────────────────────────┘ │
│ │ │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Services Layer │ │
│ │ - inventory_service.py │ │
│ │ - pnl_service.py │ │
│ │ - trade_sync_service.py │ │
│ │ - rate_limiter_service.py │ │
│ └──────────────────────────────────────────────────────┘ │
│ │ │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ External API Integration Layer │ │
│ │ - steam_api.py (OAuth, inventory, trades) │ │
│ │ - csfloat_scraper.py (price scraping) │ │
│ └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────┐
│ External APIs (100% Free) │
│ │
│ ┌───────────────────────────┐ │
│ │ Steam Web API │ │
│ │ - IPlayerService │ │
│ │ - ISteamUser │ │
│ │ - IEconService │ │
│ └───────────────────────────┘ │
│ │
│ ┌───────────────────────────┐ │
│ │ CSFloat (Scraping) │ │
│ │ - Market listings │ │
│ │ - Real-time prices │ │
│ └───────────────────────────┘ │
└─────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Database (SQLite/PostgreSQL) │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Tables: │ │
│ │ - users (Steam accounts) │ │
│ │ - items (inventory items) │ │
│ │ - trades (trade history) │ │
│ │ - inventory_snapshots (value over time) │ │
│ │ - price_cache (CSFloat prices cache) │ │
│ └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

text

### 3.2 Data Flow Diagram

**1. User Login Flow:**
User clicks "Login with Steam"
↓
Redirect to Steam OAuth
↓
User authorizes app
↓
Steam returns to callback URL with auth code
↓
Backend exchanges code for access token
↓
Store user Steam ID in database
↓
Redirect to dashboard

text

**2. Inventory Sync Flow:**
User lands on dashboard
↓
Frontend requests /api/inventory
↓
Backend checks last sync time
↓
If >5 minutes ago, fetch from Steam API
↓
For each item, get price from CSFloat (cache if available)
↓
Store/update items in database
↓
Return inventory with current prices to frontend
↓
Frontend displays inventory + total value

text

**3. Trade History Sync Flow:**
User clicks "Sync Trades"
↓
Backend calls Steam API IEconService/GetTradeHistory
↓
Paginate through trade history (50 trades/page)
↓
For each trade:

Detect BUY or SELL

Extract item details

Calculate price & fees
↓
Store trades in database
↓
Calculate P&L using FIFO algorithm
↓
Return P&L summary to frontend

text

**4. P&L Calculation Flow:**
Get all trades for user (sorted by timestamp ASC)
↓
For each SELL trade:

Find matching BUY trade (FIFO or unique token)

Calculate profit = sell_price - buy_price - fees

Mark BUY trade as "matched"
↓
Sum all profits = Total P&L
↓
Return P&L breakdown (per item, per month, etc.)

text

---

## 4. Database Design

### 4.1 Entity-Relationship Diagram (ERD)

┌─────────────────────────────────────────────────────────────────┐
│ users │
├─────────────────────────────────────────────────────────────────┤
│ PK id INTEGER │
│ steam_id VARCHAR(17) UNIQUE │
│ steam_username VARCHAR(255) │
│ avatar_url TEXT │
│ created_at TIMESTAMP │
│ updated_at TIMESTAMP │
└─────────────────────────────────────────────────────────────────┘
│
│ 1:N
▼
┌─────────────────────────────────────────────────────────────────┐
│ items │
├─────────────────────────────────────────────────────────────────┤
│ PK id INTEGER │
│ FK user_id INTEGER → users.id │
│ asset_id VARCHAR(255) UNIQUE │
│ name VARCHAR(255) │
│ category VARCHAR(50) │
│ rarity VARCHAR(50) │
│ float_value FLOAT │
│ pattern_index INTEGER │
│ stickers JSON │
│ inspect_link TEXT │
│ current_price FLOAT │
│ acquired_at TIMESTAMP │
│ acquired_price FLOAT │
│ sold_at TIMESTAMP (NULL if not sold) │
│ sold_price FLOAT │
│ pnl FLOAT │
│ created_at TIMESTAMP │
│ updated_at TIMESTAMP │
└─────────────────────────────────────────────────────────────────┘
│
│ 1:N
▼
┌─────────────────────────────────────────────────────────────────┐
│ trades │
├─────────────────────────────────────────────────────────────────┤
│ PK id INTEGER │
│ FK user_id INTEGER → users.id │
│ trade_id VARCHAR(255) UNIQUE │
│ trade_type VARCHAR(10) ("BUY" or "SELL") │
│ item_name VARCHAR(255) │
│ item_asset_id VARCHAR(255) │
│ price FLOAT │
│ fee FLOAT │
│ net_amount FLOAT │
│ timestamp TIMESTAMP │
│ created_at TIMESTAMP │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ inventory_snapshots │
├─────────────────────────────────────────────────────────────────┤
│ PK id INTEGER │
│ FK user_id INTEGER → users.id │
│ total_value FLOAT │
│ total_items INTEGER │
│ snapshot_date DATE │
│ created_at TIMESTAMP │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ price_cache │
├─────────────────────────────────────────────────────────────────┤
│ PK id INTEGER │
│ item_name VARCHAR(255) UNIQUE │
│ price FLOAT │
│ cached_at TIMESTAMP │
└─────────────────────────────────────────────────────────────────┘

text

### 4.2 Table Schemas (SQL)

**users table:**
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
items table:

sql
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
trades table:

sql
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
inventory_snapshots table:

sql
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
price_cache table:

sql
CREATE TABLE price_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_price_cache_name ON price_cache(item_name);
CREATE INDEX idx_price_cache_time ON price_cache(cached_at);
4.3 Database Migration Strategy
Using Alembic:

Initialize Alembic:

bash
alembic init alembic
Configure alembic.ini:

text
sqlalchemy.url = sqlite:///./cs2_tracker.db
Create initial migration:

bash
alembic revision --autogenerate -m "Initial schema"
Apply migration:

bash
alembic upgrade head
Future changes:

bash
# Modify models.py
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
5. API Integration Plan
5.1 Steam API Integration
Documentation: https://developer.valvesoftware.com/wiki/Steam_Web_API

5.1.1 Get Steam API Key
Steps:

Go to: https://steamcommunity.com/dev/apikey

Register domain (use localhost for development)

Get API key (format: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX)

Store in .env: STEAM_API_KEY=your_key_here

Limitations:

✅ 100% FREE (no rate limit for personal use)

⚠️ Rate limit: ~100 requests/minute (soft limit, not enforced strictly)

⚠️ Some endpoints require user authentication (OAuth)

5.1.2 Steam OAuth Login
Endpoint: https://steamcommunity.com/openid/login

Flow:

python
# Step 1: Redirect user to Steam login
redirect_url = "https://steamcommunity.com/openid/login?" + urlencode({
    "openid.ns": "http://specs.openid.net/auth/2.0",
    "openid.mode": "checkid_setup",
    "openid.return_to": "http://localhost:8000/auth/callback",
    "openid.realm": "http://localhost:8000",
    "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
    "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
})

# Step 2: User authorizes, Steam redirects to callback
# Step 3: Validate OpenID response
# Step 4: Extract Steam ID from claimed_id
steam_id = claimed_id.split("/")[-1]
Security:

✅ Use HTTPS in production

✅ Validate openid.signed parameter

✅ Check openid.mode == "id_res"

5.1.3 Get User Inventory
Endpoint: https://steamcommunity.com/inventory/{steam_id}/730/2

Parameters:

steam_id: User's 64-bit Steam ID

730: CS2 App ID

2: Context ID (2 = in-game items)

count: Items per page (default 5000, max 5000)

start_assetid: Pagination cursor (optional)

Response Structure:

json
{
  "assets": [
    {
      "appid": 730,
      "contextid": "2",
      "assetid": "123456789",
      "classid": "987654321",
      "instanceid": "0",
      "amount": "1"
    }
  ],
  "descriptions": [
    {
      "appid": 730,
      "classid": "987654321",
      "instanceid": "0",
      "market_hash_name": "AK-47 | Slate (Field-Tested)",
      "name": "AK-47 | Slate",
      "type": "Rifle",
      "tradable": 1,
      "marketable": 1,
      "commodity": 0,
      "market_fee_app": 730,
      "icon_url": "...",
      "descriptions": [
        {
          "value": "Exterior: Field-Tested"
        }
      ],
      "actions": [
        {
          "link": "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S%owner_steamid%A%assetid%D...",
          "name": "Inspect in Game..."
        }
      ]
    }
  ],
  "total_inventory_count": 150,
  "success": 1,
  "rwgrsn": -2
}
Code Example:

python
import httpx

async def get_steam_inventory(steam_id: str) -> dict:
    url = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
    params = {"count": 5000}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()
5.1.4 Get Trade History
Endpoint: https://api.steampowered.com/IEconService/GetTradeHistory/v1/

Parameters:

key: Steam API key

max_trades: Number of trades to return (default 100, max 500)

start_after_time: Unix timestamp (for pagination)

start_after_tradeid: Trade ID (for pagination)

get_descriptions: 1 (include item descriptions)

language: en (language code)

include_failed: 0 (exclude failed trades)

include_total: 1 (include total count)

Authentication: Requires user OAuth token (not just API key!)

Response Structure:

json
{
  "response": {
    "trades": [
      {
        "tradeid": "123456789",
        "steamid_other": "76561198...",
        "time_init": 1707811200,
        "status": 3,
        "assets_received": [
          {
            "appid": 730,
            "contextid": "2",
            "assetid": "123456",
            "amount": "1",
            "classid": "987654"
          }
        ],
        "assets_given": []
      }
    ],
    "more": false,
    "total_trades": 150
  }
}
Code Example:

python
async def get_trade_history(api_key: str, max_trades: int = 100) -> dict:
    url = "https://api.steampowered.com/IEconService/GetTradeHistory/v1/"
    params = {
        "key": api_key,
        "max_trades": max_trades,
        "get_descriptions": 1,
        "language": "en",
        "include_failed": 0,
        "include_total": 1
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()
Pagination Strategy:

python
async def fetch_all_trades(api_key: str) -> list:
    all_trades = []
    start_time = 0
    
    while True:
        params = {
            "key": api_key,
            "max_trades": 500,
            "start_after_time": start_time,
            "get_descriptions": 1
        }
        
        response = await client.get(url, params=params)
        data = response.json()
        trades = data["response"]["trades"]
        
        if not trades:
            break
            
        all_trades.extend(trades)
        start_time = trades[-1]["time_init"]
        
        if not data["response"]["more"]:
            break
            
        await asyncio.sleep(1)  # Rate limiting
    
    return all_trades
5.2 CSFloat API Integration (Scraping)
Website: https://csfloat.com

Note: CSFloat does NOT have official public API. We must scrape HTML.

5.2.1 Scraping Strategy
Approach:

✅ Use httpx + BeautifulSoup4 (not Selenium - too slow)

✅ Cache prices for 5-10 minutes (reduce requests)

✅ Rotate user agents (avoid detection)

✅ Add delays between requests (2-5 seconds)

✅ Use proxies if needed (optional)

Target URL Pattern:

text
https://csfloat.com/search?market_hash_name={item_name}
Example:

text
https://csfloat.com/search?market_hash_name=AK-47%20%7C%20Slate%20%28Field-Tested%29
5.2.2 HTML Structure
Price Location:

xml
<div class="price">
  <span class="amount">$7.30</span>
</div>
Code Example:

python
from bs4 import BeautifulSoup
import httpx

async def get_csfloat_price(item_name: str) -> float:
    url = "https://csfloat.com/search"
    params = {"market_hash_name": item_name}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers, timeout=15.0)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        price_element = soup.select_one('.price .amount')
        
        if price_element:
            price_text = price_element.text.strip().replace('$', '')
            return float(price_text)
        
        return 0.0
5.2.3 Anti-Scraping Protection
CSFloat Protection:

✅ Cloudflare (sometimes)

✅ Rate limiting (too many requests = temporary ban)

✅ User agent check

Bypass Strategy:

python
# 1. Rotate User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

# 2. Add Delays
import asyncio
await asyncio.sleep(random.uniform(2, 5))

# 3. Cache Prices
from functools import lru_cache
from datetime import datetime, timedelta

price_cache = {}

async def get_cached_price(item_name: str) -> float:
    if item_name in price_cache:
        cached_price, cached_time = price_cache[item_name]
        if datetime.now() - cached_time < timedelta(minutes=5):
            return cached_price
    
    price = await get_csfloat_price(item_name)
    price_cache[item_name] = (price, datetime.now())
    return price
5.2.4 Fallback: Steam Market Prices
If CSFloat scraping fails, use Steam Market API:

Endpoint: https://steamcommunity.com/market/priceoverview/

Parameters:

appid: 730

market_hash_name: Item name

currency: 1 (USD)

Response:

json
{
  "success": true,
  "lowest_price": "$7.30",
  "volume": "150",
  "median_price": "$7.50"
}
Code Example:

python
async def get_steam_market_price(item_name: str) -> float:
    url = "https://steamcommunity.com/market/priceoverview/"
    params = {
        "appid": 730,
        "market_hash_name": item_name,
        "currency": 1
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=10.0)
        data = response.json()
        
        if data.get("success"):
            price_text = data.get("lowest_price", "$0.00").replace('$', '')
            return float(price_text)
        
        return 0.0
5.3 Rate Limiting Strategy
Goal: Avoid Steam/CSFloat bans

Implementation:

python
from collections import deque
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = timedelta(seconds=time_window)
        self.requests = deque()
    
    async def acquire(self):
        now = datetime.now()
        
        # Remove old requests outside time window
        while self.requests and now - self.requests > self.time_window:
            self.requests.popleft()
        
        # If at limit, wait
        if len(self.requests) >= self.max_requests:
            sleep_time = (self.requests + self.time_window - now).total_seconds()
            await asyncio.sleep(sleep_time)
            return await self.acquire()
        
        self.requests.append(now)

# Usage
steam_limiter = RateLimiter(max_requests=60, time_window=60)  # 60 req/min
csfloat_limiter = RateLimiter(max_requests=20, time_window=60)  # 20 req/min

async def fetch_with_limit(url: str, limiter: RateLimiter):
    await limiter.acquire()
    async with httpx.AsyncClient() as client:
        return await client.get(url)
6. Core Features Implementation
6.1 Inventory Tracking
Goal: Fetch user inventory and calculate total value

Workflow:

text
1. Fetch inventory from Steam API
2. Parse item details (name, float, pattern, stickers)
3. Get prices from CSFloat (with cache)
4. Store items in database
5. Calculate total value
6. Return to frontend
Code Structure:

backend/app/services/inventory.py:

python
from sqlalchemy.orm import Session
from app.api import steam, csfloat
from app.models import Item
from typing import List, Dict

class InventoryService:
    def __init__(self, db: Session):
        self.db = db
    
    async def sync_inventory(self, user_id: int, steam_id: str) -> List[Dict]:
        # 1. Fetch from Steam
        inventory_data = await steam.get_inventory(steam_id)
        
        # 2. Parse items
        items = []
        for asset in inventory_data["assets"]:
            description = self._find_description(
                asset["classid"], 
                inventory_data["descriptions"]
            )
            
            # 3. Get price (with cache)
            price = await csfloat.get_cached_price(description["market_hash_name"])
            
            # 4. Parse float & pattern
            float_value, pattern = self._parse_inspect_link(description)
            
            # 5. Create/update item
            item = Item(
                user_id=user_id,
                asset_id=asset["assetid"],
                name=description["market_hash_name"],
                category=description["type"],
                rarity=self._extract_rarity(description),
                float_value=float_value,
                pattern_index=pattern,
                current_price=price,
                inspect_link=self._get_inspect_link(description)
            )
            
            items.append(item)
        
        # 6. Bulk upsert
        self._bulk_upsert(items)
        
        # 7. Calculate total
        total_value = sum(item.current_price for item in items)
        
        return {
            "items": items,
            "total_value": total_value,
            "total_items": len(items)
        }
    
    def _find_description(self, classid: str, descriptions: List) -> Dict:
        for desc in descriptions:
            if desc["classid"] == classid:
                return desc
        return {}
    
    def _parse_inspect_link(self, description: Dict) -> tuple:
        # Extract float & pattern from inspect link
        # Implementation: Use regex to parse inspect link
        return (0.0, 0)  # Placeholder
    
    def _extract_rarity(self, description: Dict) -> str:
        # Extract rarity from tags
        for tag in description.get("tags", []):
            if tag["category"] == "Rarity":
                return tag["name"]
        return "Unknown"
    
    def _bulk_upsert(self, items: List[Item]):
        # Use SQLAlchemy bulk operations
        pass
6.2 P&L Calculation
Goal: Calculate profit/loss for all trades

Algorithm:

FIFO (First-In-First-Out) for Consumables:

text
Consumables: Cases, Keys, Capsules (fungible items)

Example:
BUY 10 keys @ $2.50 = $25.00
BUY 5 keys @ $2.60 = $13.00
SELL 7 keys @ $2.70 = $18.90

FIFO Matching:
- Sell 7 keys matches first 7 from first purchase ($2.50 each)
- Cost basis = 7 × $2.50 = $17.50
- Profit = $18.90 - $17.50 = $1.40
Unique Token for Skins:

text
Skins: Each skin has unique inspect link (token)

Example:
BUY AK-47 Slate (float 0.164, pattern 123) @ $5.19
SELL AK-47 Slate (float 0.164, pattern 123) @ $7.30

Matching:
- Exact match via inspect link
- Profit = $7.30 - $5.19 - $0.95 (13% fee) = $1.16
Code Structure:

backend/app/services/pnl.py:

python
from sqlalchemy.orm import Session
from app.models import Trade, Item
from typing import List, Dict
from collections import deque

class PnLService:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_pnl(self, user_id: int) -> Dict:
        trades = self.db.query(Trade).filter(
            Trade.user_id == user_id
        ).order_by(Trade.timestamp.asc()).all()
        
        consumable_pnl = self._calculate_fifo_pnl(trades)
        skin_pnl = self._calculate_unique_pnl(trades)
        
        total_pnl = consumable_pnl + skin_pnl
        
        return {
            "total_pnl": total_pnl,
            "consumable_pnl": consumable_pnl,
            "skin_pnl": skin_pnl,
            "breakdown": self._get_breakdown(trades)
        }
    
    def _calculate_fifo_pnl(self, trades: List[Trade]) -> float:
        """FIFO for cases, keys, capsules"""
        inventory = {}  # {item_name: deque[(price, quantity)]}
        total_pnl = 0.0
        
        for trade in trades:
            if not self._is_consumable(trade.item_name):
                continue
            
            if trade.trade_type == "BUY":
                if trade.item_name not in inventory:
                    inventory[trade.item_name] = deque()
                inventory[trade.item_name].append((trade.price, 1))
            
            elif trade.trade_type == "SELL":
                if trade.item_name not in inventory or not inventory[trade.item_name]:
                    continue
                
                buy_price, _ = inventory[trade.item_name].popleft()
                profit = trade.net_amount - buy_price
                total_pnl += profit
        
        return total_pnl
    
    def _calculate_unique_pnl(self, trades: List[Trade]) -> float:
        """Unique token matching for skins"""
        buy_map = {}  # {asset_id: buy_trade}
        total_pnl = 0.0
        
        for trade in trades:
            if self._is_consumable(trade.item_name):
                continue
            
            if trade.trade_type == "BUY":
                buy_map[trade.item_asset_id] = trade
            
            elif trade.trade_type == "SELL":
                if trade.item_asset_id not in buy_map:
                    continue
                
                buy_trade = buy_map[trade.item_asset_id]
                profit = trade.net_amount - buy_trade.price
                total_pnl += profit
                
                del buy_map[trade.item_asset_id]
        
        return total_pnl
    
    def _is_consumable(self, item_name: str) -> bool:
        consumables = ["Case", "Key", "Capsule", "Sticker Capsule"]
        return any(c in item_name for c in consumables)
    
    def _get_breakdown(self, trades: List[Trade]) -> List[Dict]:
        # Return per-item P&L breakdown
        pass
6.3 Trade History Sync
Goal: Fetch 1 year of trade history from Steam

Challenges:

✅ Steam API returns max 500 trades per request

✅ Must paginate using start_after_time + start_after_tradeid

✅ Rate limiting (60 req/min)

Code Structure:

backend/app/services/trade_sync.py:

python
from sqlalchemy.orm import Session
from app.api import steam
from app.models import Trade
from datetime import datetime, timedelta
import asyncio

class TradeSyncService:
    def __init__(self, db: Session):
        self.db = db
    
    async def sync_trades(self, user_id: int, api_key: str, days_back: int = 365) -> int:
        start_time = int((datetime.now() - timedelta(days=days_back)).timestamp())
        all_trades = []
        
        while True:
            trades_data = await steam.get_trade_history(
                api_key=api_key,
                max_trades=500,
                start_after_time=start_time
            )
            
            trades = trades_data["response"]["trades"]
            
            if not trades:
                break
            
            # Parse and store
            for trade in trades:
                trade_obj = self._parse_trade(user_id, trade)
                all_trades.append(trade_obj)
            
            # Pagination
            start_time = trades[-1]["time_init"]
            
            if not trades_data["response"]["more"]:
                break
            
            # Rate limit
            await asyncio.sleep(1)
        
        # Bulk insert
        self._bulk_insert(all_trades)
        
        return len(all_trades)
    
    def _parse_trade(self, user_id: int, trade_data: Dict) -> Trade:
        # Detect BUY or SELL
        is_buy = len(trade_data["assets_received"]) > 0
        trade_type = "BUY" if is_buy else "SELL"
        
        # Extract first item (simplified)
        assets = trade_data["assets_received"] if is_buy else trade_data["assets_given"]
        
        if not assets:
            return None
        
        asset = assets
        
        # Find description
        description = self._find_description(asset["classid"], trade_data.get("descriptions", []))
        
        return Trade(
            user_id=user_id,
            trade_id=trade_data["tradeid"],
            trade_type=trade_type,
            item_name=description.get("market_hash_name", "Unknown"),
            item_asset_id=asset["assetid"],
            price=self._estimate_price(description),  # Estimate from market
            fee=0.0,  # Calculate based on platform
            net_amount=0.0,
            timestamp=datetime.fromtimestamp(trade_data["time_init"])
        )
    
    def _find_description(self, classid: str, descriptions: List) -> Dict:
        for desc in descriptions:
            if desc["classid"] == classid:
                return desc
        return {}
    
    def _estimate_price(self, description: Dict) -> float:
        # Get historical price (simplified - use current price for now)
        return 0.0
    
    def _bulk_insert(self, trades: List[Trade]):
        self.db.bulk_save_objects(trades)
        self.db.commit()
6.4 Inventory Snapshots
Goal: Track inventory value over time (daily snapshots)

Workflow:

text
1. Run daily cron job (or user-triggered)
2. Calculate total inventory value
3. Store snapshot in database
4. Display as line chart on dashboard
Code:

backend/app/services/inventory.py (add method):

python
from app.models import InventorySnapshot
from datetime import date

async def create_snapshot(self, user_id: int) -> InventorySnapshot:
    items = self.db.query(Item).filter(
        Item.user_id == user_id,
        Item.sold_at.is_(None)  # Only unsold items
    ).all()
    
    total_value = sum(item.current_price for item in items)
    total_items = len(items)
    
    snapshot = InventorySnapshot(
        user_id=user_id,
        total_value=total_value,
        total_items=total_items,
        snapshot_date=date.today()
    )
    
    self.db.add(snapshot)
    self.db.commit()
    
    return snapshot
Cron Job (FastAPI Background Task):

python
from fastapi_utils.tasks import repeat_every

@app.on_event("startup")
@repeat_every(seconds=86400)  # Daily
async def daily_snapshot():
    db = SessionLocal()
    inventory_service = InventoryService(db)
    
    users = db.query(User).all()
    for user in users:
        await inventory_service.create_snapshot(user.id)
    
    db.close()
7. Frontend Design
7.1 Dashboard Layout
Wireframe:

text
┌─────────────────────────────────────────────────────────────────┐
│  Header                                                          │
│  [Logo]  CS2 Tracker          [Sync] [Accounts ▾] [Logout]      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Stats Cards                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Total Value  │  │ Total P&L    │  │ Total Items  │          │
│  │   $1,234.56  │  │   +$234.56   │  │     142      │          │
│  │   ↑ 12.5%    │  │   ↑ 45.2%    │  │   ↑ 5        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Inventory Value Over Time                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                          │    │
│  │    [Line Chart: Value vs Date]                          │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Current Inventory                                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ [Search]  [Filter: All ▾]  [Sort: Value ▾]              │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │ [Icon] AK-47 | Slate (FT)         Float: 0.164  $7.30   │    │
│  │ [Icon] Glock-18 | Fade (FN)       Float: 0.008  $450.00 │    │
│  │ [Icon] Sticker | device           -              $5.20   │    │
│  │ ...                                                      │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Recent Trades                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Date       Type  Item                        P&L         │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │ 2026-02-12 SELL  AK-47 | Slate (FT)        +$2.11       │    │
│  │ 2026-02-10 BUY   Glock-18 | Fade (FN)      -            │    │
│  │ 2026-02-08 SELL  Sticker | device          +$1.50       │    │
│  │ ...                                                      │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
7.2 Technologies
HTML Structure:

xml
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CS2 Tracker - Dashboard</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Alpine.js CDN -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Axios CDN -->
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body class="bg-gray-100" x-data="dashboardData()">
    <!-- Content here -->
</body>
</html>
Alpine.js Dashboard Data:

javascript
function dashboardData() {
    return {
        user: null,
        inventory: [],
        totalValue: 0,
        totalPnL: 0,
        loading: false,
        
        async init() {
            await this.fetchUser();
            await this.fetchInventory();
            await this.fetchPnL();
        },
        
        async fetchUser() {
            const response = await axios.get('/api/user');
            this.user = response.data;
        },
        
        async fetchInventory() {
            this.loading = true;
            const response = await axios.get('/api/inventory');
            this.inventory = response.data.items;
            this.totalValue = response.data.total_value;
            this.loading = false;
        },
        
        async fetchPnL() {
            const response = await axios.get('/api/pnl');
            this.totalPnL = response.data.total_pnl;
        },
        
        async syncInventory() {
            this.loading = true;
            await axios.post('/api/inventory/sync');
            await this.fetchInventory();
        }
    }
}
Chart.js Configuration:

javascript
// Inventory value over time chart
const ctx = document.getElementById('valueChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Portfolio Value',
            data: ,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
            fill: false
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Inventory Value Over Time'
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                ticks: {
                    callback: function(value) {
                        return '$' + value.toFixed(2);
                    }
                }
            }
        }
    }
});
7.3 Responsive Design
Mobile Breakpoints (Tailwind):

xml
<!-- Desktop: 3 columns -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- Stats cards -->
</div>

<!-- Mobile: Stack vertically -->
<div class="flex flex-col space-y-4 md:space-y-0 md:flex-row md:space-x-4">
    <!-- Content -->
</div>
8. Security & Rate Limiting
8.1 Security Best Practices
1. Environment Variables:

python
# Never hardcode API keys!
# ❌ BAD:
STEAM_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# ✅ GOOD:
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    steam_api_key: str
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
2. Input Validation:

python
from pydantic import BaseModel, validator

class SteamIDInput(BaseModel):
    steam_id: str
    
    @validator('steam_id')
    def validate_steam_id(cls, v):
        if not v.isdigit() or len(v) != 17:
            raise ValueError('Invalid Steam ID format')
        return v
3. CORS Configuration:

python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
4. SQL Injection Prevention:

python
# SQLAlchemy ORM automatically prevents SQL injection
# ✅ GOOD:
user = db.query(User).filter(User.steam_id == steam_id).first()

# ❌ BAD (raw SQL):
db.execute(f"SELECT * FROM users WHERE steam_id = '{steam_id}'")
8.2 Rate Limiting Implementation
Strategy:

Steam API: 60 requests/minute

CSFloat scraping: 20 requests/minute

Dashboard endpoints: 100 requests/minute (per user)

Code:

backend/app/services/rate_limiter.py:

python
from collections import deque
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        """
        Args:
            max_requests: Max requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = timedelta(seconds=time_window)
        self.requests = deque()
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Wait if rate limit exceeded"""
        async with self.lock:
            now = datetime.now()
            
            # Remove old requests
            while self.requests and now - self.requests > self.time_window:
                self.requests.popleft()
            
            # If at limit, calculate wait time
            if len(self.requests) >= self.max_requests:
                oldest_request = self.requests
                wait_until = oldest_request + self.time_window
                wait_seconds = (wait_until - now).total_seconds()
                
                if wait_seconds > 0:
                    await asyncio.sleep(wait_seconds)
                    return await self.acquire()  # Retry after waiting
            
            # Add current request
            self.requests.append(now)

# Create global limiters
steam_limiter = RateLimiter(max_requests=60, time_window=60)
csfloat_limiter = RateLimiter(max_requests=20, time_window=60)

# Usage in API calls
async def fetch_with_limit(url: str, limiter: RateLimiter):
    await limiter.acquire()
    async with httpx.AsyncClient() as client:
        return await client.get(url)
FastAPI Dependency:

python
from fastapi import Depends, HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/inventory")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def get_inventory(request: Request):
    # Implementation
    pass
9. Deployment Strategy
9.1 Local Development
Steps:

bash
# 1. Clone repo
git clone https://github.com/yourusername/cs2-tracker.git
cd cs2-tracker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your Steam API key

# 5. Initialize database
cd backend
alembic upgrade head

# 6. Run backend
uvicorn app.main:app --reload --port 8000

# 7. Open frontend (in another terminal)
cd frontend
python -m http.server 3000

# 8. Access app
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:3000
9.2 Production Deployment (Railway)
Why Railway:

✅ Free tier (500 hours/month)

✅ PostgreSQL included (free 1GB)

✅ Auto-deploy from GitHub

✅ Zero DevOps setup

Steps:

1. Prepare for deployment:

Procfile:

text
web: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
runtime.txt:

text
python-3.10.8
railway.json:

json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
2. Deploy to Railway:

bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to GitHub repo
railway link

# Add PostgreSQL
railway add postgresql

# Deploy
railway up
3. Set environment variables:

bash
# In Railway dashboard or CLI
railway variables set STEAM_API_KEY=your_key_here
railway variables set SECRET_KEY=your_secret_key
railway variables set DATABASE_URL=postgresql://...  # Auto-set by Railway
4. Run migrations:

bash
railway run alembic upgrade head
9.3 Alternative: Docker Deployment
Dockerfile:

text
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
docker-compose.yml:

text
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/cs2_tracker
      - STEAM_API_KEY=${STEAM_API_KEY}
    depends_on:
      - db
    volumes:
      - ./backend:/app/backend
      - ./frontend:/app/frontend
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=cs2_tracker
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
Run:

bash
docker-compose up -d
10. Development Roadmap
Phase 1: MVP (Week 1-2)
Goals:

✅ Steam OAuth login

✅ Fetch current inventory

✅ Display inventory with CSFloat prices

✅ Basic dashboard UI

Tasks:

Setup project structure ✅

Implement Steam OAuth ✅

Implement inventory fetch ✅

Implement CSFloat scraper ✅

Create database models ✅

Build basic dashboard ✅

Deploy locally ✅

Success Criteria:

User can login with Steam

User sees their inventory with current prices

Dashboard loads in <2 seconds

Phase 2: Core Features (Week 3-4)
Goals:

✅ Trade history sync

✅ P&L calculation

✅ Inventory value over time

✅ Multi-account support

Tasks:

Implement trade history sync ✅

Implement FIFO P&L algorithm ✅

Implement unique token matching ✅

Add inventory snapshots ✅

Build P&L dashboard ✅

Add multi-account switcher ✅

Success Criteria:

Sync 1 year trade history in <5 minutes

Accurate P&L calculation (verified manually)

Line chart shows inventory value over time

Phase 3: Polish & Deploy (Week 5-6)
Goals:

✅ AI rate limiter

✅ Export data (CSV)

✅ Mobile-responsive design

✅ Deploy to production

Tasks:

Implement AI rate limiter ✅

Add CSV export ✅

Optimize mobile UI ✅

Add loading states ✅

Deploy to Railway ✅

Write documentation ✅

Success Criteria:

Zero API bans (smart rate limiting)

Dashboard works on mobile

Deployed and accessible remotely

Phase 4: Advanced Features (Future)
Ideas:

Price alerts (Discord/Email)

Trade recommendations (ML model)

Portfolio comparison (vs market)

Advanced charts (Plotly)

Dark mode

Multi-language support

11. Code Examples
11.1 Complete FastAPI App Structure
backend/app/main.py:

python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.database import engine
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(
    title="CS2 Trading Tracker",
    description="Track your CS2 inventory & P&L",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router, prefix="/api")

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
backend/app/api/routes.py:

python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.inventory import InventoryService
from app.services.pnl import PnLService
from app.services.trade_sync import TradeSyncService

router = APIRouter()

@router.post("/auth/callback")
async def steam_callback(openid_response: dict, db: Session = Depends(get_db)):
    # Validate Steam OpenID response
    # Extract Steam ID
    # Create/update user in database
    # Return user data
    pass

@router.get("/inventory")
async def get_inventory(user_id: int, db: Session = Depends(get_db)):
    service = InventoryService(db)
    inventory = await service.sync_inventory(user_id, steam_id)
    return inventory

@router.post("/inventory/sync")
async def sync_inventory(user_id: int, db: Session = Depends(get_db)):
    service = InventoryService(db)
    await service.sync_inventory(user_id, steam_id)
    return {"status": "synced"}

@router.get("/pnl")
async def get_pnl(user_id: int, db: Session = Depends(get_db)):
    service = PnLService(db)
    pnl = service.calculate_pnl(user_id)
    return pnl

@router.post("/trades/sync")
async def sync_trades(user_id: int, api_key: str, db: Session = Depends(get_db)):
    service = TradeSyncService(db)
    count = await service.sync_trades(user_id, api_key)
    return {"trades_synced": count}
11.2 Database Models
backend/app/models.py:

python
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
    
    user = relationship("User", back_populates="trades")

class InventorySnapshot(Base):
    __tablename__ = "inventory_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_value = Column(Float, nullable=False)
    total_items = Column(Integer, nullable=False)
    snapshot_date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="snapshots")

class PriceCache(Base):
    __tablename__ = "price_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    cached_at = Column(DateTime, default=datetime.utcnow, index=True)
11.3 Database Connection
backend/app/database.py:

python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
11.4 Configuration
backend/app/config.py:

python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CS2 Tracker"
    debug: bool = True
    secret_key: str
    database_url: str
    steam_api_key: str
    steam_web_api_url: str = "https://api.steampowered.com"
    csfloat_base_url: str = "https://csfloat.com"
    max_requests_per_minute: int = 60
    rate_limit_enabled: bool = True
    cache_enabled: bool = True
    cache_ttl: int = 3600
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
12. Testing Strategy
12.1 Unit Tests
backend/tests/test_inventory.py:

python
import pytest
from app.services.inventory import InventoryService
from app.models import User, Item
from app.database import SessionLocal

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def sample_user(db):
    user = User(steam_id="76561198012345678", steam_username="TestUser")
    db.add(user)
    db.commit()
    return user

def test_sync_inventory(db, sample_user):
    service = InventoryService(db)
    result = await service.sync_inventory(sample_user.id, sample_user.steam_id)
    
    assert result["total_items"] > 0
    assert result["total_value"] >= 0
    assert len(result["items"]) == result["total_items"]

def test_calculate_total_value(db, sample_user):
    # Add test items
    items = [
        Item(user_id=sample_user.id, asset_id="123", name="Test Item 1", current_price=10.0),
        Item(user_id=sample_user.id, asset_id="456", name="Test Item 2", current_price=20.0)
    ]
    db.bulk_save_objects(items)
    db.commit()
    
    service = InventoryService(db)
    total = service._calculate_total_value(sample_user.id)
    
    assert total == 30.0
12.2 Integration Tests
Test full workflow:

python
def test_full_workflow(db):
    # 1. Create user
    user = User(steam_id="76561198012345678")
    db.add(user)
    db.commit()
    
    # 2. Sync inventory
    inventory_service = InventoryService(db)
    inventory = await inventory_service.sync_inventory(user.id, user.steam_id)
    assert inventory["total_items"] > 0
    
    # 3. Sync trades
    trade_service = TradeSyncService(db)
    trades_count = await trade_service.sync_trades(user.id, STEAM_API_KEY)
    assert trades_count > 0
    
    # 4. Calculate P&L
    pnl_service = PnLService(db)
    pnl = pnl_service.calculate_pnl(user.id)
    assert "total_pnl" in pnl
    
    # 5. Create snapshot
    snapshot = await inventory_service.create_snapshot(user.id)
    assert snapshot.total_value > 0
12.3 Manual Testing Checklist
Before Release:

 Steam login works

 Inventory syncs correctly

 Prices update from CSFloat

 Trade history syncs (1 year)

 P&L calculation accurate

 Charts display correctly

 Multi-account switching works

 Mobile responsive

 No API bans (test rate limiting)

 Database migrations work

 Deployment successful

 Error handling works

 Loading states display

 Export CSV works

13. Troubleshooting Guide
13.1 Common Issues
Issue: "Steam API returns 403 Forbidden"

Cause: Invalid API key or rate limiting

Solution:

python
# Verify API key
print(settings.steam_api_key)  # Should be 32-char hex string

# Check rate limiting
await steam_limiter.acquire()  # Use limiter before API call

# Add retry logic
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def fetch_steam_api(url):
    response = await client.get(url)
    response.raise_for_status()
    return response.json()
Issue: "CSFloat scraping returns empty prices"

Cause: HTML structure changed or anti-scraping protection

Solution:

python
# 1. Inspect current HTML structure
response = await client.get(url)
print(response.text)  # Check HTML

# 2. Update selector
soup = BeautifulSoup(response.text, 'lxml')
price_element = soup.select_one('.new-selector-here')  # Update selector

# 3. Fallback to Steam Market API
if not price_element:
    price = await get_steam_market_price(item_name)
Issue: "Database migration fails"

Cause: Schema mismatch or existing data conflict

Solution:

bash
# 1. Check migration status
alembic current

# 2. If stuck, downgrade and re-upgrade
alembic downgrade -1
alembic upgrade head

# 3. If database corrupted (development only!), reset
rm cs2_tracker.db
alembic upgrade head
Issue: "Rate limit exceeded (429 error)"

Cause: Too many requests to Steam/CSFloat

Solution:

python
# 1. Increase wait time in rate limiter
steam_limiter = RateLimiter(max_requests=30, time_window=60)  # 30 req/min instead of 60

# 2. Add exponential backoff
import random

async def fetch_with_backoff(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                await asyncio.sleep(wait_time)
            else:
                raise
Issue: "Frontend not loading data"

Cause: CORS issue or API endpoint error

Solution:

python
# 1. Check CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Check API endpoint
@app.get("/api/inventory")
async def get_inventory():
    return {"items": [], "total_value": 0}  # Test with dummy data

# 3. Check browser console for errors
# Open DevTools (F12) → Console tab
Issue: "P&L calculation incorrect"

Cause: FIFO algorithm bug or missing trades

Solution:

python
# 1. Debug FIFO algorithm
def _calculate_fifo_pnl(self, trades):
    print(f"Total trades: {len(trades)}")
    
    for trade in trades:
        print(f"Trade: {trade.trade_type} {trade.item_name} @ ${trade.price}")
    
    # ... rest of algorithm

# 2. Verify trade data
trades = db.query(Trade).filter(Trade.user_id == user_id).all()
for trade in trades:
    print(f"{trade.timestamp} | {trade.trade_type} | {trade.item_name} | ${trade.price}")

# 3. Manual verification
# Export trades to CSV, calculate P&L in Excel, compare results
13.2 Performance Optimization
Issue: "Dashboard loads slowly (>5 seconds)"

Solutions:

1. Add database indexes:

python
# In models.py
class Item(Base):
    # ...
    __table_args__ = (
        Index('idx_user_name', 'user_id', 'name'),
        Index('idx_user_sold', 'user_id', 'sold_at'),
    )
2. Use lazy loading:

python
# Don't load all data at once
@app.get("/api/inventory")
async def get_inventory(page: int = 1, per_page: int = 50):
    offset = (page - 1) * per_page
    items = db.query(Item).limit(per_page).offset(offset).all()
    return {"items": items, "page": page}
3. Cache API responses:

python
from functools import lru_cache
from datetime import datetime, timedelta

cache = {}

@lru_cache(maxsize=128)
async def get_cached_inventory(user_id: int, ttl: int = 300):
    cache_key = f"inventory:{user_id}"
    
    if cache_key in cache:
        data, timestamp = cache[cache_key]
        if datetime.now() - timestamp < timedelta(seconds=ttl):
            return data
    
    data = await fetch_inventory(user_id)
    cache[cache_key] = (data, datetime.now())
    return data
4. Use async everywhere:

python
# ❌ BAD (blocking)
def get_price(item_name):
    response = requests.get(url)
    return response.json()

# ✅ GOOD (async)
async def get_price(item_name):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
13.3 Debugging Tips
1. Enable detailed logging:

python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# In code
logger.debug(f"Fetching inventory for user {user_id}")
logger.info(f"Synced {len(trades)} trades")
logger.error(f"Failed to fetch price: {e}")
2. Use FastAPI debug mode:

bash
uvicorn app.main:app --reload --log-level debug
3. Inspect database:

bash
sqlite3 cs2_tracker.db

# SQL commands
.tables
SELECT * FROM users;
SELECT COUNT(*) FROM items;
SELECT * FROM trades ORDER BY timestamp DESC LIMIT 10;
4. Test API endpoints:

bash
# Using curl
curl http://localhost:8000/api/inventory

# Using httpie (better formatting)
http GET http://localhost:8000/api/inventory

# Using FastAPI auto-docs
# Open: http://localhost:8000/docs
14. Next Steps
After Blueprint Complete
1. Start Coding:

Create project structure

Implement Phase 1 (MVP)

Test locally

Deploy

2. Iterate:

Get user feedback

Fix bugs

Add features

Optimize performance

3. Scale:

Add more accounts

Support other games (Dota 2, TF2)

Build mobile app

Monetize (premium features)

15. Resources
Documentation Links
Steam API:

Official Docs: https://developer.valvesoftware.com/wiki/Steam_Web_API

API Key: https://steamcommunity.com/dev/apikey

OpenID Guide: https://steamcommunity.com/dev

FastAPI:

Docs: https://fastapi.tiangolo.com/

Tutorial: https://fastapi.tiangolo.com/tutorial/

SQLAlchemy:

Docs: https://docs.sqlalchemy.org/

ORM Tutorial: https://docs.sqlalchemy.org/en/20/orm/quickstart.html

Tailwind CSS:

Docs: https://tailwindcss.com/docs

Chart.js:

Docs: https://www.chartjs.org/docs/

Alpine.js:

Docs: https://alpinejs.dev/start-here

Community
Discord:

r/csgomarketforum Discord

CS2 Trading Community

Reddit:

r/csgomarketforum

r/GlobalOffensive

r/FastAPI

GitHub:

Search: "cs2 inventory tracker"

Search: "steam api python"

16. License & Credits
License: MIT (or your choice)

Credits:

Steam Web API (Valve)

CSFloat (market data)

FastAPI (web framework)

Chart.js (charts library)