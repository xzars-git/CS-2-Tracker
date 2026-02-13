import asyncio
import sys
sys.path.insert(0, 'app')

from app.database import SessionLocal
from app.models import User, Item
from app.services.steam import SteamService
from datetime import datetime

async def manual_sync():
    """Manually sync inventory for user with correct Steam ID"""
    
    db = SessionLocal()
    
    try:
        # Get user
        user = db.query(User).order_by(User.id.desc()).first()
        
        print(f"📋 User Info:")
        print(f"  User ID: {user.id}")
        print(f"  Steam ID: {user.steam_id}")
        print(f"  Username: {user.steam_username}")
        print("=" * 60)
        
        # Verify Steam ID
        expected_steam_id = "76561199629904226"
        if user.steam_id != expected_steam_id:
            print(f"⚠️ WARNING: Steam ID mismatch!")
            print(f"  Expected: {expected_steam_id}")
            print(f"  Got: {user.steam_id}")
            return
        
        print(f"\n✅ Steam ID correct!\n")
        
        # Fetch inventory
        steam_service = SteamService()
        print(f"🔄 Fetching inventory from Steam...")
        
        inventory_data = await steam_service.get_inventory(user.steam_id)
        
        if "error" in inventory_data:
            print(f"❌ Error: {inventory_data['error']}")
            return
        
        items_from_steam = inventory_data.get("items", [])
        print(f"✅ Fetched {len(items_from_steam)} items from Steam\n")
        
        if not items_from_steam:
            print("⚠️ No items in inventory")
            return
        
        # Display items
        print("📦 Items found:")
        for i, item in enumerate(items_from_steam, 1):
            tradable = "✅" if item.get('tradable') else "🔒"
            print(f"{i}. {item['name']} {tradable}")
        
        # Save to database
        print(f"\n💾 Saving to database...")
        
        # Delete old items for this user
        db.query(Item).filter(Item.user_id == user.id).delete()
        
        # Add new items
        for steam_item in items_from_steam:
            item = Item(
                user_id=user.id,
                asset_id=steam_item["asset_id"],
                name=steam_item["name"],
                category=steam_item.get("category"),
                rarity=steam_item.get("rarity"),
                icon_url=steam_item.get("icon_url"),
                acquired_at=datetime.utcnow(),
                current_price=0.0
            )
            db.add(item)
        
        db.commit()
        
        # Verify
        item_count = db.query(Item).filter(Item.user_id == user.id).count()
        print(f"✅ Saved {item_count} items to database\n")
        
        print("=" * 60)
        print("🎉 SYNC COMPLETE!")
        print(f"User {user.id} now has {item_count} items")
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(manual_sync())
