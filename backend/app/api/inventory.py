from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Item
from app.services.steam import SteamService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_inventory(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Get current inventory for a user from database
    
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
        "items": [
            {
                "id": item.id,
                "asset_id": item.asset_id,
                "name": item.name,
                "category": item.category,
                "rarity": item.rarity,
                "float_value": item.float_value,
                "icon_url": item.icon_url,
                "current_price": item.current_price,
                "acquired_at": item.acquired_at,
            }
            for item in items
        ],
        "total_value": round(total_value, 2),
        "total_items": len(items)
    }


async def sync_inventory_task(user_id: int, steam_id: str, db: Session):
    """Background task to sync inventory"""
    from app.services.price import PriceService
    
    steam_service = SteamService()
    price_service = PriceService()
    
    try:
        logger.info(f"Starting inventory sync for user {user_id}")
        
        # Fetch inventory from Steam
        inventory_data = await steam_service.get_inventory(steam_id)
        
        if "error" in inventory_data:
            logger.error(f"Failed to sync inventory for user {user_id}: {inventory_data['error']}")
            return
        
        items_from_steam = inventory_data.get("items", [])
        logger.info(f"Fetched {len(items_from_steam)} items from Steam for user {user_id}")
        
        # Get existing items from database
        existing_items = db.query(Item).filter(
            Item.user_id == user_id,
            Item.sold_at.is_(None)
        ).all()
        
        existing_asset_ids = {item.asset_id for item in existing_items}
        new_asset_ids = {item["asset_id"] for item in items_from_steam}
        
        # Add new items
        new_items_added = 0
        for steam_item in items_from_steam:
            if steam_item["asset_id"] not in existing_asset_ids:
                item = Item(
                    user_id=user_id,
                    asset_id=steam_item["asset_id"],
                    name=steam_item["name"],
                    category=steam_item.get("category"),
                    rarity=steam_item.get("rarity"),
                    icon_url=steam_item.get("icon_url"),
                    acquired_at=datetime.utcnow(),
                    current_price=0.0  # Will be updated below
                )
                db.add(item)
                new_items_added += 1
        
        # Mark sold items (items in DB but not in Steam inventory)
        sold_items = 0
        for item in existing_items:
            if item.asset_id not in new_asset_ids:
                item.sold_at = datetime.utcnow()
                sold_items += 1
        
        db.commit()
        logger.info(f"Synced inventory for user {user_id}: {new_items_added} new, {sold_items} sold")
        
        # Fetch prices for all items
        logger.info(f"Fetching prices for {len(items_from_steam)} items...")
        unique_item_names = list(set(item["name"] for item in items_from_steam))
        
        # Fetch prices (with rate limiting built in)
        prices = await price_service.bulk_fetch_prices(unique_item_names[:50], db)  # Limit to 50 to avoid timeout
        logger.info(f"Fetched prices for {len(prices)} items")
        
        # Update item prices
        updated_prices = 0
        for item in db.query(Item).filter(
            Item.user_id == user_id,
            Item.sold_at.is_(None)
        ).all():
            if item.name in prices:
                item.current_price = prices[item.name]
                updated_prices += 1
        
        db.commit()
        logger.info(f"Updated prices for {updated_prices} items for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error syncing inventory for user {user_id}: {e}")
        db.rollback()


@router.post("/sync")
async def sync_inventory(
    user_id: int = Query(..., description="User ID"),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Sync inventory from Steam API
    
    Fetches latest inventory and updates database
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Run sync in background
    if background_tasks:
        background_tasks.add_task(sync_inventory_task, user_id, user.steam_id, db)
        return {
            "status": "syncing",
            "message": "Inventory sync started in background"
        }
    else:
        # Sync immediately (for testing)
        await sync_inventory_task(user_id, user.steam_id, db)
        return {
            "status": "completed",
            "message": "Inventory synced successfully"
        }
