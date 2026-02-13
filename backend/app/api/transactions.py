from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app.models import Trade, User
from app.utils.user_helpers import get_user_int_id
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


# Pydantic schemas
class TransactionCreate(BaseModel):
    item_name: str
    trade_type: str  # "BUY" or "SELL"
    price: float
    fee: Optional[float] = 0.0
    timestamp: datetime
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    item_name: str
    trade_type: str
    price: float
    fee: float
    net_amount: float
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class PnLStats(BaseModel):
    total_bought: float
    total_sold: float
    total_profit: float
    total_fees: float
    net_profit: float
    transaction_count: int
    profitable_trades: int
    losing_trades: int


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    user_id: str = Query(..., description="User Unique ID"),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction (buy or sell)
    """
    # Validate trade type
    if transaction.trade_type not in ["BUY", "SELL"]:
        raise HTTPException(status_code=400, detail="trade_type must be 'BUY' or 'SELL'")
    
    # Calculate net amount
    # Fee only applies to Steam Market transactions (will be set during import)
    if transaction.trade_type == "BUY":
        net_amount = -(transaction.price + (transaction.fee or 0))  # Negative for buys
    else:
        net_amount = transaction.price - (transaction.fee or 0)  # Positive for sells
    
    # Resolve user ID
    int_user_id = get_user_int_id(user_id, db)
    
    # Generate unique trade ID
    trade_id = f"{int_user_id}_{transaction.item_name}_{int(transaction.timestamp.timestamp())}"
    
    # Create transaction (manual source, no auto-fee)
    new_trade = Trade(
        user_id=int_user_id,
        trade_id=trade_id,
        trade_type=transaction.trade_type,
        item_name=transaction.item_name,
        price=transaction.price,
        fee=transaction.fee or 0,
        net_amount=net_amount,
        source="manual",  # Manual entry
        timestamp=transaction.timestamp
    )
    
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    
    logger.info(f"Created transaction {new_trade.id} for user {user_id}")
    
    return new_trade


@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    user_id: str = Query(..., description="User Unique ID"),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    trade_type: Optional[str] = Query(None, description="Filter by BUY or SELL"),
    db: Session = Depends(get_db)
):
    """
    Get all transactions for a user
    """
    int_user_id = get_user_int_id(user_id, db)
    query = db.query(Trade).filter(Trade.user_id == int_user_id)
    
    if trade_type:
        query = query.filter(Trade.trade_type == trade_type)
    
    transactions = query.order_by(desc(Trade.timestamp)).offset(offset).limit(limit).all()
    
    return transactions


@router.get("/pnl", response_model=PnLStats)
async def get_pnl(
    user_id: str = Query(..., description="User Unique ID"),
    db: Session = Depends(get_db)
):
    """
    Calculate P&L statistics for user
    """
    int_user_id = get_user_int_id(user_id, db)
    # Get all transactions
    transactions = db.query(Trade).filter(Trade.user_id == int_user_id).all()
    
    if not transactions:
        return PnLStats(
            total_bought=0,
            total_sold=0,
            total_profit=0,
            total_fees=0,
            net_profit=0,
            transaction_count=0,
            profitable_trades=0,
            losing_trades=0
        )
    
    total_bought = 0
    total_sold = 0
    total_fees = 0
    
    # Calculate totals
    for trade in transactions:
        total_fees += trade.fee or 0
        
        if trade.trade_type == "BUY":
            total_bought += trade.price
        else:
            total_sold += trade.price
    
    # Calculate per-item P&L
    item_pnl = {}
    for trade in transactions:
        item = trade.item_name
        if item not in item_pnl:
            item_pnl[item] = {"buys": [], "sells": []}
        
        if trade.trade_type == "BUY":
            item_pnl[item]["buys"].append(trade.price)
        else:
            item_pnl[item]["sells"].append(trade.price)
    
    # Calculate profitable vs losing trades
    profitable = 0
    losing = 0
    
    for item, data in item_pnl.items():
        buys = data["buys"]
        sells = data["sells"]
        
        # Match sells with buys (FIFO)
        for sell_price in sells:
            if buys:
                buy_price = buys.pop(0)
                if sell_price > buy_price:
                    profitable += 1
                elif sell_price < buy_price:
                    losing += 1
    
    total_profit = total_sold - total_bought
    net_profit = total_profit - total_fees
    
    return PnLStats(
        total_bought=total_bought,
        total_sold=total_sold,
        total_profit=total_profit,
        total_fees=total_fees,
        net_profit=net_profit,
        transaction_count=len(transactions),
        profitable_trades=profitable,
        losing_trades=losing
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Get a specific transaction
    """
    transaction = db.query(Trade).filter(
        Trade.id == transaction_id,
        Trade.user_id == user_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return transaction


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Delete a transaction
    """
    transaction = db.query(Trade).filter(
        Trade.id == transaction_id,
        Trade.user_id == user_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    
    return {"message": "Transaction deleted successfully"}


@router.get("/items/summary")
async def get_items_summary(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Get P&L summary per item
    """
    transactions = db.query(Trade).filter(Trade.user_id == user_id).all()
    
    item_summary = {}
    
    for trade in transactions:
        item = trade.item_name
        if item not in item_summary:
            item_summary[item] = {
                "item_name": item,
                "total_bought": 0,
                "total_sold": 0,
                "buy_count": 0,
                "sell_count": 0,
                "pnl": 0,
                "avg_buy_price": 0,
                "avg_sell_price": 0
            }
        
        if trade.trade_type == "BUY":
            item_summary[item]["total_bought"] += trade.price
            item_summary[item]["buy_count"] += 1
        else:
            item_summary[item]["total_sold"] += trade.price
            item_summary[item]["sell_count"] += 1
    
    # Calculate averages and P&L
    for item, data in item_summary.items():
        if data["buy_count"] > 0:
            data["avg_buy_price"] = data["total_bought"] / data["buy_count"]
        if data["sell_count"] > 0:
            data["avg_sell_price"] = data["total_sold"] / data["sell_count"]
        
        data["pnl"] = data["total_sold"] - data["total_bought"]
    
    # Sort by P&L descending
    sorted_items = sorted(item_summary.values(), key=lambda x: x["pnl"], reverse=True)
    
    return sorted_items
