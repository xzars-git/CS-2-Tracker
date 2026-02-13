import asyncio
import httpx

async def test_correct_steam_id():
    """Test inventory with correct Steam ID"""
    
    # CORRECT Steam ID from user
    steam_id = "76561199629904226"
    
    print(f"Testing with CORRECT Steam ID: {steam_id}")
    print("=" * 60)
    
    url = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
    params = {
        "count": 100,
        "l": "english"
    }
    
    print(f"URL: {url}\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=15.0)
            
            print(f"Status Code: {response.status_code}\n")
            
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    print(f"❌ API Error: {data['error']}")
                else:
                    assets = data.get("assets", [])
                    descriptions = data.get("descriptions", [])
                    
                    print(f"✅ SUCCESS!")
                    print(f"Assets: {len(assets)}")
                    print(f"Descriptions: {len(descriptions)}\n")
                    
                    if assets:
                        # Create description map
                        desc_map = {
                            f"{d['classid']}_{d['instanceid']}": d 
                            for d in descriptions
                        }
                        
                        print("First 10 items:")
                        for i, asset in enumerate(assets[:10], 1):
                            key = f"{asset['classid']}_{asset['instanceid']}"
                            desc = desc_map.get(key, {})
                            
                            name = desc.get("market_hash_name", "Unknown")
                            tradable = desc.get("tradable", 0)
                            
                            print(f"{i}. {name}")
                            print(f"   Tradable: {'Yes' if tradable == 1 else 'No (LOCKED 🔒)'}")
                        
                        # Count locked items
                        locked = sum(1 for a in assets if desc_map.get(f"{a['classid']}_{a['instanceid']}", {}).get("tradable", 0) != 1)
                        print(f"\n📊 Summary:")
                        print(f"Total items: {len(assets)}")
                        print(f"Trade-locked: {locked}")
                        print(f"Tradable: {len(assets) - locked}")
                        
            elif response.status_code == 403:
                print("❌ 403 - Inventory is PRIVATE")
            elif response.status_code == 401:
                print("❌ 401 - Unauthorized (wrong Steam ID?)")
            elif response.status_code == 500:
                print("⚠️ 500 - No CS2 items or Steam error")
            else:
                print(f"❌ Status {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_correct_steam_id())
