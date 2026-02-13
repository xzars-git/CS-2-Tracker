import asyncio
import sys
sys.path.insert(0, 'app')

from app.database import SessionLocal
from app.models import User
from app.services.steam import SteamService

async def test_user_inventory():
    """Test fetching inventory for logged-in user"""
    
    db = SessionLocal()
    
    try:
        # Get the most recent user
        user = db.query(User).order_by(User.id.desc()).first()
        
        if not user:
            print("❌ No users found in database")
            return
        
        print(f"Testing inventory for user:")
        print(f"  ID: {user.id}")
        print(f"  Steam ID: {user.steam_id}")
        print(f"  Username: {user.steam_username}")
        print("=" * 60)
        
        steam_service = SteamService()
        
        print(f"\nFetching inventory from Steam API...")
        inventory_data = await steam_service.get_inventory(user.steam_id)
        
        if "error" in inventory_data:
            print(f"\n❌ Error: {inventory_data['error']}")
            print("\n📝 Troubleshooting:")
            print("1. Make sure your Steam Profile is PUBLIC")
            print("   https://steamcommunity.com/profiles/{}/edit/settings".format(user.steam_id))
            print("\n2. Make sure your Inventory is PUBLIC")
            print("   Go to: Privacy Settings → Inventory → Set to Public")
            print("\n3. Check your inventory URL:")
            print(f"   https://steamcommunity.com/inventory/{user.steam_id}/730/2")
            return
        
        items = inventory_data.get("items", [])
        print(f"\n✅ Successfully fetched {len(items)} items!")
        
        if items:
            print(f"\n📦 Sample items (first 10):")
            for i, item in enumerate(items[:10], 1):
                tradable = "✅" if item.get('tradable') else "🔒"
                print(f"\n{i}. {item['name']}")
                print(f"   {tradable} Tradable: {item.get('tradable', False)}")
                print(f"   Category: {item.get('category', 'N/A')}")
                print(f"   Rarity: {item.get('rarity', 'N/A')}")
            
            # Count trade-locked items
            locked_count = sum(1 for item in items if not item.get('tradable', False))
            print(f"\n📊 Summary:")
            print(f"   Total items: {len(items)}")
            print(f"   Trade-locked: {locked_count}")
            print(f"   Tradable: {len(items) - locked_count}")
        else:
            print("\n⚠️ No items found in inventory")
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_user_inventory())
