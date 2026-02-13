import httpx
import asyncio

async def test_direct_inventory_url():
    """Test if we can access inventory directly via Steam Community API"""
    
    # Try different possible Steam IDs
    test_ids = [
        "76561199964226984",  # From earlier test
    ]
    
    for steam_id in test_ids:
        print(f"\n{'='*60}")
        print(f"Testing Steam ID: {steam_id}")
        print(f"{'='*60}")
        
        # Test inventory URL
        url = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
        params = {
            "count": 100,
            "l": "english"
        }
        
        print(f"\nInventory URL: {url}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=15.0, follow_redirects=True)
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "error" in data:
                        print(f"❌ API Error: {data['error']}")
                    else:
                        assets = data.get("assets", [])
                        descriptions = data.get("descriptions", [])
                        
                        print(f"✅ Success!")
                        print(f"   Assets found: {len(assets)}")
                        print(f"   Descriptions: {len(descriptions)}")
                        
                        if assets:
                            print(f"\n📦 First 3 items:")
                            # Create description map
                            desc_map = {
                                f"{d['classid']}_{d['instanceid']}": d 
                                for d in descriptions
                            }
                            
                            for i, asset in enumerate(assets[:3], 1):
                                key = f"{asset['classid']}_{asset['instanceid']}"
                                desc = desc_map.get(key, {})
                                
                                name = desc.get("market_hash_name", "Unknown")
                                tradable = desc.get("tradable", 0)
                                
                                print(f"   {i}. {name}")
                                print(f"      Asset ID: {asset['assetid']}")
                                print(f"      Tradable: {'Yes' if tradable == 1 else 'No (locked)'}")
                        
                        return True  # Success
                        
                elif response.status_code == 403:
                    print(f"❌ 403 Forbidden - Inventory is PRIVATE")
                elif response.status_code == 500:
                    print(f"⚠️ 500 Server Error - Steam API issue or no CS2 items")
                else:
                    print(f"❌ Unexpected status code")
                    print(f"Response text: {response.text[:200]}")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    return False

if __name__ == "__main__":
    asyncio.run(test_direct_inventory_url())
