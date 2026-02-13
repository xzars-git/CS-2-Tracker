import httpx
import asyncio

async def test_steam_api():
    """Test Steam API player summary endpoint"""
    
    api_key = "451FD1052803656243EF8999A7335CC2"
    test_steam_id = "76561198033388536"  # Example Steam ID
    
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        "key": api_key,
        "steamids": test_steam_id
    }
    
    print(f"Testing Steam API...")
    print(f"URL: {url}")
    print(f"Steam ID: {test_steam_id}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                data = response.json()
                players = data.get("response", {}).get("players", [])
                if players:
                    print("\n✅ Success! Player data:")
                    print(f"Username: {players[0].get('personaname')}")
                    print(f"Avatar: {players[0].get('avatarfull')}")
                else:
                    print("\n⚠️ No player data returned")
            else:
                print(f"\n❌ Error: HTTP {response.status_code}")
                
    except Exception as e:
        print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_steam_api())
