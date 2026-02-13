from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Item
from app.services.price import PriceService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/update")
async def update_prices(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Update prices for user's inventory items
    
    Fetches latest prices from CSFloat/Steam Market
    """
    price_service = PriceService()
    
    # Get user's current inventory
    items = db.query(Item).filter(
        Item.user_id == user_id,
        Item.sold_at.is_(None)
    ).all()
    
    if not items:
        return {
            "status": "success",
            "message": "No items to update",
            "updated": 0
        }
    
    # Get unique item names
    unique_names = list(set(item.name for item in items))
    
    logger.info(f"Updating prices for {len(unique_names)} unique items for user {user_id}")
    
    # Fetch prices
    prices = await price_service.bulk_fetch_prices(unique_names[:100], db)
    
    # Update items
    updated = 0
    for item in items:
        if item.name in prices:
            item.current_price = prices[item.name]
            updated += 1
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Updated prices for {updated} items",
        "updated": updated,
        "total_items": len(items)
    }


@router.get("/price/{item_name}")
async def get_item_price(
    item_name: str,
    db: Session = Depends(get_db)
):
    """
    Get current market price for a specific item
    
    Args:
        item_name: Market hash name of the item
        
    Returns:
        Current price from CSFloat or Steam Market
    """
    price_service = PriceService()
    
    price = await price_service.get_item_price(item_name, db)
    
    if price:
        return {
            "item_name": item_name,
            "price": price,
            "currency": "USD"
        }
    else:
        return {
            "item_name": item_name,
            "price": None,
            "error": "Price not found"
        }
