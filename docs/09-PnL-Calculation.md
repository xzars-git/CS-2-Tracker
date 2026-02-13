# 09 - P&L Calculation

**CS2 Trading Tracker - Profit & Loss Calculation Logic**

---

## 9.1 P&L Calculation Overview

### Two Algorithms:

1. **FIFO (First-In-First-Out)** - For consumables
   - Cases, Keys, Capsules
   - Fungible items (identical)

2. **Unique Token Matching** - For skins
   - AK-47, AWP, Glock, etc.
   - Each skin has unique float + pattern

---

## 9.2 FIFO Algorithm (Consumables)

### How It Works:
```
BUY 10 keys @ $2.50 = $25.00
BUY 5 keys @ $2.60 = $13.00
SELL 7 keys @ $2.70 = $18.90

FIFO Matching:
- Sell 7 keys matches first 7 from first purchase ($2.50 each)
- Cost basis = 7 × $2.50 = $17.50
- Profit = $18.90 - $17.50 = $1.40
```

### Python Implementation:
```python
from collections import deque
from typing import List, Dict

def calculate_fifo_pnl(trades: List[Dict]) -> float:
    """
    Calculate P&L using FIFO for consumables
    
    Args:
        trades: List of trades sorted by timestamp ASC
        
    Returns:
        Total P&L for consumables
    """
    inventory = {}  # {item_name: deque[(price, quantity)]}
    total_pnl = 0.0
    
    for trade in trades:
        # Skip non-consumables
        if not is_consumable(trade["item_name"]):
            continue
        
        item_name = trade["item_name"]
        
        if trade["trade_type"] == "BUY":
            # Add to inventory queue
            if item_name not in inventory:
                inventory[item_name] = deque()
            inventory[item_name].append((trade["price"], 1))
        
        elif trade["trade_type"] == "SELL":
            # Pop from queue (FIFO)
            if item_name not in inventory or not inventory[item_name]:
                continue  # Can't sell what you don't have
            
            buy_price, _ = inventory[item_name].popleft()
            profit = trade["net_amount"] - buy_price
            total_pnl += profit
    
    return total_pnl

def is_consumable(item_name: str) -> bool:
    """Check if item is consumable (fungible)"""
    consumables = ["Case", "Key", "Capsule", "Sticker Capsule", "Pin"]
    return any(c in item_name for c in consumables)
```

---

## 9.3 Unique Token Matching (Skins)

### How It Works:
```
BUY AK-47 Slate (float 0.164, pattern 123) @ $5.19
SELL AK-47 Slate (float 0.164, pattern 123) @ $7.30

Matching:
- Exact match via asset_id
- Profit = $7.30 - $5.19 - $0.95 (fee) = $1.16
```

### Python Implementation:
```python
def calculate_unique_pnl(trades: List[Dict]) -> float:
    """
    Calculate P&L using unique token matching for skins
    
    Args:
        trades: List of trades sorted by timestamp ASC
        
    Returns:
        Total P&L for skins
    """
    buy_map = {}  # {asset_id: buy_trade}
    total_pnl = 0.0
    
    for trade in trades:
        # Skip consumables
        if is_consumable(trade["item_name"]):
            continue
        
        asset_id = trade["item_asset_id"]
        
        if trade["trade_type"] == "BUY":
            # Store buy trade by asset_id
            buy_map[asset_id] = trade
        
        elif trade["trade_type"] == "SELL":
            # Find matching buy trade
            if asset_id not in buy_map:
                continue  # Sold item we didn't buy (gift, etc.)
            
            buy_trade = buy_map[asset_id]
            profit = trade["net_amount"] - buy_trade["price"]
            total_pnl += profit
            
            # Remove from buy map
            del buy_map[asset_id]
    
    return total_pnl
```

---

## 9.4 Complete P&L Service

### `backend/app/services/pnl.py`:
```python
from sqlalchemy.orm import Session
from app.models import Trade, Item
from typing import Dict, List
from collections import deque

class PnLService:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_pnl(self, user_id: int) -> Dict:
        """
        Calculate total P&L for user
        
        Returns:
            {
                "total_pnl": float,
                "consumable_pnl": float,
                "skin_pnl": float,
                "breakdown": List[Dict]
            }
        """
        # Get all trades sorted by timestamp
        trades = self.db.query(Trade).filter(
            Trade.user_id == user_id
        ).order_by(Trade.timestamp.asc()).all()
        
        # Convert to dict for processing
        trades_data = [
            {
                "trade_type": t.trade_type,
                "item_name": t.item_name,
                "item_asset_id": t.item_asset_id,
                "price": t.price,
                "fee": t.fee,
                "net_amount": t.net_amount,
                "timestamp": t.timestamp
            }
            for t in trades
        ]
        
        # Calculate P&L
        consumable_pnl = self._calculate_fifo_pnl(trades_data)
        skin_pnl = self._calculate_unique_pnl(trades_data)
        total_pnl = consumable_pnl + skin_pnl
        
        return {
            "total_pnl": round(total_pnl, 2),
            "consumable_pnl": round(consumable_pnl, 2),
            "skin_pnl": round(skin_pnl, 2),
            "breakdown": self._get_breakdown(trades_data)
        }
    
    def _calculate_fifo_pnl(self, trades: List[Dict]) -> float:
        """FIFO for consumables"""
        inventory = {}
        total_pnl = 0.0
        
        for trade in trades:
            if not self._is_consumable(trade["item_name"]):
                continue
            
            item_name = trade["item_name"]
            
            if trade["trade_type"] == "BUY":
                if item_name not in inventory:
                    inventory[item_name] = deque()
                inventory[item_name].append((trade["price"], 1))
            
            elif trade["trade_type"] == "SELL":
                if item_name not in inventory or not inventory[item_name]:
                    continue
                
                buy_price, _ = inventory[item_name].popleft()
                profit = trade["net_amount"] - buy_price
                total_pnl += profit
        
        return total_pnl
    
    def _calculate_unique_pnl(self, trades: List[Dict]) -> float:
        """Unique token matching for skins"""
        buy_map = {}
        total_pnl = 0.0
        
        for trade in trades:
            if self._is_consumable(trade["item_name"]):
                continue
            
            asset_id = trade["item_asset_id"]
            
            if trade["trade_type"] == "BUY":
                buy_map[asset_id] = trade
            
            elif trade["trade_type"] == "SELL":
                if asset_id not in buy_map:
                    continue
                
                buy_trade = buy_map[asset_id]
                profit = trade["net_amount"] - buy_trade["price"]
                total_pnl += profit
                
                del buy_map[asset_id]
        
        return total_pnl
    
    def _is_consumable(self, item_name: str) -> bool:
        """Check if item is consumable"""
        consumables = ["Case", "Key", "Capsule", "Sticker Capsule", "Pin"]
        return any(c in item_name for c in consumables)
    
    def _get_breakdown(self, trades: List[Dict]) -> List[Dict]:
        """Get per-item P&L breakdown"""
        breakdown = []
        buy_map = {}
        
        for trade in trades:
            if trade["trade_type"] == "BUY":
                buy_map[trade["item_asset_id"]] = trade
            
            elif trade["trade_type"] == "SELL":
                asset_id = trade["item_asset_id"]
                if asset_id in buy_map:
                    buy_trade = buy_map[asset_id]
                    pnl = trade["net_amount"] - buy_trade["price"]
                    
                    breakdown.append({
                        "item_name": trade["item_name"],
                        "buy_price": buy_trade["price"],
                        "sell_price": trade["net_amount"],
                        "pnl": round(pnl, 2),
                        "buy_date": buy_trade["timestamp"].isoformat(),
                        "sell_date": trade["timestamp"].isoformat()
                    })
        
        # Sort by PnL descending
        breakdown.sort(key=lambda x: x["pnl"], reverse=True)
        
        return breakdown
```

---

## 9.5 FastAPI Route

### `backend/app/api/routes.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.pnl import PnLService

router = APIRouter()

@router.get("/pnl")
async def get_pnl(user_id: int, db: Session = Depends(get_db)):
    """Get P&L for user"""
    service = PnLService(db)
    pnl_data = service.calculate_pnl(user_id)
    return pnl_data
```

---

## 9.6 Testing P&L Calculation

### Unit Test:
```python
import pytest
from app.services.pnl import PnLService

def test_fifo_pnl():
    """Test FIFO P&L calculation"""
    trades = [
        {"trade_type": "BUY", "item_name": "CS:GO Weapon Case", "price": 0.10, "net_amount": 0.10},
        {"trade_type": "BUY", "item_name": "CS:GO Weapon Case", "price": 0.15, "net_amount": 0.15},
        {"trade_type": "SELL", "item_name": "CS:GO Weapon Case", "price": 0.20, "net_amount": 0.20},
    ]
    
    service = PnLService(None)
    pnl = service._calculate_fifo_pnl(trades)
    
    # First case bought at $0.10, sold at $0.20
    # Expected P&L: $0.20 - $0.10 = $0.10
    assert pnl == 0.10

def test_unique_token_pnl():
    """Test unique token P&L calculation"""
    trades = [
        {"trade_type": "BUY", "item_name": "AK-47 | Slate", "item_asset_id": "123", "price": 5.00, "net_amount": 5.00},
        {"trade_type": "SELL", "item_name": "AK-47 | Slate", "item_asset_id": "123", "price": 7.00, "net_amount": 7.00},
    ]
    
    service = PnLService(None)
    pnl = service._calculate_unique_pnl(trades)
    
    # Bought at $5.00, sold at $7.00
    # Expected P&L: $7.00 - $5.00 = $2.00
    assert pnl == 2.00
```

---

## Next Steps

✅ **Lanjut ke:** [`12-Frontend-Design.md`](12-Frontend-Design.md) - Display P&L on dashboard  
✅ **Alternative:** [`18-Testing-Strategy.md`](18-Testing-Strategy.md) - Test P&L logic

---

**P&L calculation ready! 💰**
