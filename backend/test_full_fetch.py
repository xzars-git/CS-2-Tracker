import asyncio
import httpx

async def test_full_inventory():
    """Test fetching FULL inventory with pagination"""
    
    steam_id = "76561199629904226"
    
    print(f"Testing FULL inventory for: {steam_id}")
    print("=" * 60)
    
    all_items = []
    start_assetid = None
    page = 1
    
    while True:
        url = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
        params = {
            "count": 5000,
            "l": "english"
        }
        
        if start_assetid:
            params["start_assetid"] = start_assetid
        
        print(f"\n📄 Page {page}...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=30.0)
                
                if response.status_code != 200:
                    print(f"❌ Status {response.status_code}")
                    break
                
                data = response.json()
                
                if "error" in data:
                    print(f"❌ Error: {data['error']}")
                    break
                
                assets = data.get("assets", [])
                descriptions = data.get("descriptions", [])
                
                print(f"   Assets on this page: {len(assets)}")
                
                # Create description map
                desc_map = {
                    f"{d['classid']}_{d['instanceid']}": d 
                    for d in descriptions
                }
                
                # Process items
                for asset in assets:
                    key = f"{asset['classid']}_{asset['instanceid']}"
                    desc = desc_map.get(key, {})
                    
                    item = {
                        "asset_id": asset["assetid"],
                        "name": desc.get("market_hash_name", "Unknown"),
                        "tradable": desc.get("tradable", 0) == 1,
                        "category": None,
                        "rarity": None
                    }
                    
                    # Extract category and rarity from tags
                    tags = desc.get("tags", [])
                    for tag in tags:
                        if tag.get("category") == "Type":
                            item["category"] = tag.get("localized_tag_name")
                        if tag.get("category") == "Rarity":
                            item["rarity"] = tag.get("localized_tag_name")
                    
                    all_items.append(item)
                
                # Check if there are more pages
                if data.get("more_items", 0) == 1:
                    start_assetid = data.get("last_assetid")
                    page += 1
                else:
                    break
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
            break
    
    print(f"\n{'='*60}")
    print(f"✅ TOTAL ITEMS FOUND: {len(all_items)}")
    print(f"{'='*60}\n")
    
    if all_items:
        # Count by category
        categories = {}
        for item in all_items:
            cat = item.get("category", "Unknown")
            categories[cat] = categories.get(cat, 0) + 1
        
        print("📊 Items by category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")
        
        # Count tradable vs locked
        tradable = sum(1 for item in all_items if item.get("tradable"))
        locked = len(all_items) - tradable
        
        print(f"\n🔐 Trade status:")
        print(f"  Tradable: {tradable}")
        print(f"  Trade-locked: {locked}")
        
        # Show sample items
        print(f"\n📦 First 10 items:")
        for i, item in enumerate(all_items[:10], 1):
            lock = "🔒" if not item.get("tradable") else "✅"
            print(f"  {i}. {lock} {item['name']}")
    
    return all_items

if __name__ == "__main__":
    asyncio.run(test_full_inventory())
