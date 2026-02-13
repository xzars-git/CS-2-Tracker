from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Trade
from app.services.steam_market import SteamMarketService
from app.utils.user_helpers import get_user_int_id
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class ImportRequest(BaseModel):
    cookies: str
    count: Optional[int] = 500


@router.post("/steam-market")
async def import_steam_market_history(
    request: ImportRequest,
    user_id: str = Query(..., description="User Unique ID"),
    db: Session = Depends(get_db)
):
    """
    Import Steam Market transaction history using browser cookies
    
    **How to get cookies:**
    1. Open Steam Market in your browser
    2. Press F12 to open DevTools
    3. Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
    4. Click "Cookies" → "https://steamcommunity.com"
    5. Copy ALL cookies as string: "sessionid=...; steamLoginSecure=..."
    6. Paste here
    
    **Required cookies:**
    - sessionid
    - steamLoginSecure
    - steamCountry (optional but recommended)
    """
    steam_market = SteamMarketService()
    
    # Resolve user ID
    int_user_id = get_user_int_id(user_id, db)
    
    logger.info(f"Starting market history import for user {int_user_id}")
    
    # Validate cookies
    if not request.cookies or len(request.cookies) < 20:
        raise HTTPException(
            status_code=400,
            detail="Invalid cookies. Please provide complete cookie string from browser."
        )
    
    # Fetch market history
    result = await steam_market.fetch_market_history(
        cookies=request.cookies,
        count=request.count
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch market history: {result.get('error', 'Unknown error')}"
        )
    
    transactions = result.get("transactions", [])
    
    if not transactions:
        return {
            "status": "success",
            "message": "No transactions found in Steam Market history",
            "imported": 0,
            "skipped": 0,
            "total": 0
        }
    
    # Import transactions into database
    imported = 0
    skipped = 0
    
    for tx in transactions:
        try:
            # Generate unique trade ID
            trade_id = f"{int_user_id}_market_{tx['item_name']}_{int(tx['timestamp'].timestamp())}"
            
            # Check if already exists
            existing = db.query(Trade).filter(Trade.trade_id == trade_id).first()
            if existing:
                skipped += 1
                continue
            
            # Calculate net amount
            price = tx.get("price", 0)
            fee = price * 0.05  # Steam Market takes 5% fee (auto-calculated)
            
            if tx["trade_type"] == "BUY":
                net_amount = -(price + fee)
            else:
                net_amount = price - fee
            
            # Create transaction with steam_market source
            new_trade = Trade(
                user_id=int_user_id,
                trade_id=trade_id,
                trade_type=tx["trade_type"],
                item_name=tx["item_name"],
                price=price,
                fee=fee,  # Auto-calculated 5% Steam fee
                net_amount=net_amount,
                source="steam_market",  # Mark as Steam Market transaction
                timestamp=tx["timestamp"]
            )
            
            db.add(new_trade)
            imported += 1
            
        except Exception as e:
            logger.error(f"Error importing transaction: {e}")
            continue
    
    # Commit all at once
    db.commit()
    
    logger.info(f"Import complete: {imported} imported, {skipped} skipped")
    
    return {
        "status": "success",
        "message": f"Successfully imported {imported} transactions from Steam Market",
        "imported": imported,
        "skipped": skipped,
        "total": len(transactions)
    }


@router.get("/cookie-guide")
async def get_cookie_guide():
    """
    Get step-by-step guide on how to extract Steam cookies
    """
    return {
        "title": "How to Get Steam Cookies",
        "steps": [
            {
                "step": 1,
                "title": "Open Steam Market in Browser",
                "description": "Go to https://steamcommunity.com/market/ and make sure you're logged in"
            },
            {
                "step": 2,
                "title": "Open Browser DevTools",
                "description": "Press F12 on your keyboard (or right-click → Inspect)"
            },
            {
                "step": 3,
                "title": "Navigate to Cookies",
                "description": "Chrome: Application tab → Cookies → steamcommunity.com\nFirefox: Storage tab → Cookies → steamcommunity.com"
            },
            {
                "step": 4,
                "title": "Copy Cookie Values",
                "description": "Find these cookies and copy their values:\n- sessionid\n- steamLoginSecure\n- steamCountry"
            },
            {
                "step": 5,
                "title": "Format as String",
                "description": "Combine like this:\nsessionid=YOUR_VALUE; steamLoginSecure=YOUR_VALUE; steamCountry=YOUR_VALUE"
            },
            {
                "step": 6,
                "title": "Paste into Import Form",
                "description": "Paste the complete cookie string into the import form in the app"
            }
        ],
        "security_note": "⚠️ Your cookies are like your password! Never share them. They're used ONLY to fetch your own transaction history and are NOT stored.",
        "example": "sessionid=abc123...; steamLoginSecure=xyz789...; steamCountry=US"
    }
