from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Item, Trade, InventorySnapshot
from typing import List, Optional
from datetime import date

router = APIRouter()


# ============================================================================
# USER ENDPOINTS
# ============================================================================

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(User).all()
    return users


@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ============================================================================
# INVENTORY ENDPOINTS
# ============================================================================

@router.get("/inventory")
async def get_inventory(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Get current inventory for a user
    
    Returns:
        - items: List of inventory items
        - total_value: Sum of all item prices
        - total_items: Count of items
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get unsold items
    items = db.query(Item).filter(
        Item.user_id == user_id,
        Item.sold_at.is_(None)
    ).all()
    
    # Calculate total value
    total_value = sum(item.current_price or 0 for item in items)
    
    return {
        "items": items,
        "total_value": round(total_value, 2),
        "total_items": len(items)
    }


@router.post("/inventory/sync")
async def sync_inventory(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Sync inventory from Steam API
    
    TODO: Implement actual Steam API integration
    For now, returns placeholder response
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Call Steam API and update database
    return {
        "status": "pending",
        "message": "Steam API integration coming soon"
    }


# ============================================================================
# TRADE ENDPOINTS
# ============================================================================

@router.get("/trades")
async def get_trades(
    user_id: int = Query(..., description="User ID"),
    limit: int = Query(50, description="Number of trades to return"),
    db: Session = Depends(get_db)
):
    """Get trade history for a user"""
    trades = db.query(Trade).filter(
        Trade.user_id == user_id
    ).order_by(Trade.timestamp.desc()).limit(limit).all()
    
    return trades


@router.post("/trades/sync")
async def sync_trades(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Sync trade history from Steam API
    
    TODO: Implement actual Steam API integration
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Call Steam API and sync trades
    return {
        "status": "pending",
        "message": "Steam API integration coming soon"
    }


# ============================================================================
# P&L ENDPOINTS
# ============================================================================

@router.get("/pnl")
async def get_pnl(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Calculate P&L for a user
    
    TODO: Implement P&L calculation logic
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Implement FIFO and unique token matching
    return {
        "total_pnl": 0.0,
        "consumable_pnl": 0.0,
        "skin_pnl": 0.0,
        "breakdown": []
    }


# ============================================================================
# SNAPSHOT ENDPOINTS
# ============================================================================

@router.get("/snapshots")
async def get_snapshots(
    user_id: int = Query(..., description="User ID"),
    days: int = Query(30, description="Number of days to retrieve"),
    db: Session = Depends(get_db)
):
    """Get inventory value snapshots for charts"""
    snapshots = db.query(InventorySnapshot).filter(
        InventorySnapshot.user_id == user_id
    ).order_by(InventorySnapshot.snapshot_date.desc()).limit(days).all()
    
    # Reverse to get chronological order
    snapshots.reverse()
    
    return snapshots
