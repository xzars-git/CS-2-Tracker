import asyncio
import httpx

async def test_with_headers():
    """Test inventory fetch with proper headers"""
    
    steam_id = "76561199629904226"
    
    print(f"Testing inventory for: {steam_id}")
    print("=" * 60)
    
    # Try different approaches
    
    # Approach 1: Standard API call
    print("\n🔍 Approach 1: Standard API")
    url1 = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
    params1 = {"count": 5000, "l": "english"}
    
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url1, params=params1, timeout=30.0)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                assets = data.get("assets", [])
                print(f"   ✅ Items: {len(assets)}")
            else:
                print(f"   ❌ Failed: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Approach 2: With proper user agent
    print("\n🔍 Approach 2: With User-Agent")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
            response = await client.get(url1, params=params1, timeout=30.0)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                assets = data.get("assets", [])
                print(f"   ✅ Items: {len(assets)}")
            else:
                print(f"   ❌ Failed: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Approach 3: Alternative endpoint
    print("\n🔍 Approach 3: Alternative endpoint")
    url3 = f"https://steamcommunity.com/profiles/{steam_id}/inventory/json/730/2"
    
    try:
        async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
            response = await client.get(url3, timeout=30.0)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        rgInventory = data.get("rgInventory", {})
                        print(f"   ✅ Items: {len(rgInventory)}")
                    else:
                        print(f"   ⚠️ Unexpected format")
                except:
                    print(f"   ⚠️ Not JSON")
            else:
                print(f"   ❌ Failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Approach 4: Direct browser simulation
    print("\n🔍 Approach 4: Full browser headers")
    headers_full = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://steamcommunity.com/profiles/{steam_id}/inventory/",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        async with httpx.AsyncClient(headers=headers_full, follow_redirects=True) as client:
            response = await client.get(url1, params=params1, timeout=30.0)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                assets = data.get("assets", [])
                descriptions = data.get("descriptions", [])
                print(f"   ✅ Assets: {len(assets)}")
                print(f"   ✅ Descriptions: {len(descriptions)}")
                
                if assets:
                    print(f"\n   📦 First 5 items:")
                    desc_map = {f"{d['classid']}_{d['instanceid']}": d for d in descriptions}
                    
                    for i, asset in enumerate(assets[:5], 1):
                        key = f"{asset['classid']}_{asset['instanceid']}"
                        desc = desc_map.get(key, {})
                        name = desc.get("market_hash_name", "Unknown")
                        print(f"   {i}. {name}")
            else:
                print(f"   ❌ Failed: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_with_headers())
