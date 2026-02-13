import asyncio
import sys
sys.path.insert(0, 'app')

from app.services.steam import SteamService

async def test_inventory():
    """Test fetching inventory for a specific Steam ID"""
    
    # Your Steam ID from the login
    steam_id = "76561199964226984"  # User_904256 -> last part of Steam64 ID
    
    steam_service = SteamService()
    
    print(f"Testing inventory fetch for Steam ID: {steam_id}")
    print("=" * 60)
    
    try:
        inventory_data = await steam_service.get_inventory(steam_id)
        
        if "error" in inventory_data:
            print(f"❌ Error: {inventory_data['error']}")
            return
        
        items = inventory_data.get("items", [])
        print(f"✅ Successfully fetched {len(items)} items\n")
        
        if items:
            # Show first 5 items
            print("First 5 items:")
            for i, item in enumerate(items[:5], 1):
                print(f"\n{i}. {item['name']}")
                print(f"   Asset ID: {item['asset_id']}")
                print(f"   Category: {item.get('category', 'N/A')}")
                print(f"   Rarity: {item.get('rarity', 'N/A')}")
                print(f"   Tradable: {item.get('tradable', False)}")
                print(f"   Marketable: {item.get('marketable', False)}")
        else:
            print("⚠️ No items found")
            print("\nPossible reasons:")
            print("1. Inventory is private")
            print("2. No CS2 items in inventory")
            print("3. Steam API issue")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_inventory())
