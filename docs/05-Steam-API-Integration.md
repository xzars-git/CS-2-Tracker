# 05 - Steam API Integration

**CS2 Trading Tracker - Steam Web API Setup**

---

## 5.1 Getting Started with Steam API

### Get Your Steam API Key:
1. Go to: https://steamcommunity.com/dev/apikey
2. Register domain: `localhost` (for development)
3. Get API key: `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
4. Store in `.env`: `STEAM_API_KEY=your_key_here`

### Limitations:
- ✅ **100% FREE** (no rate limit for personal use)
- ⚠️ **Soft limit:** ~100 requests/minute
- ⚠️ Some endpoints require user OAuth

---

## 5.2 Steam OAuth Login

### Endpoint:
```
https://steamcommunity.com/openid/login
```

### Python Implementation:
```python
from urllib.parse import urlencode
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/auth/login")
async def steam_login():
    """Redirect user to Steam login page"""
    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": "http://localhost:8000/auth/callback",
        "openid.realm": "http://localhost:8000",
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
    }
    
    redirect_url = "https://steamcommunity.com/openid/login?" + urlencode(params)
    return RedirectResponse(redirect_url)

@app.get("/auth/callback")
async def steam_callback(request: Request):
    """Handle Steam OAuth callback"""
    # Get query parameters
    params = dict(request.query_params)
    
    # Validate OpenID response
    if params.get("openid.mode") != "id_res":
        raise HTTPException(status_code=400, detail="Invalid OpenID response")
    
    # Extract Steam ID from claimed_id
    # Format: https://steamcommunity.com/openid/id/76561198012345678
    claimed_id = params.get("openid.claimed_id", "")
    steam_id = claimed_id.split("/")[-1]
    
    # Create/update user in database
    # ... (see database module)
    
    return {"steam_id": steam_id}
```

### Security Checklist:
- ✅ Use HTTPS in production
- ✅ Validate `openid.signed` parameter
- ✅ Check `openid.mode == "id_res"`
- ✅ Verify Steam ID format (17 digits)

---

## 5.3 Get User Inventory

### Endpoint:
```
https://steamcommunity.com/inventory/{steam_id}/730/2
```

### Parameters:
- `steam_id`: User's 64-bit Steam ID
- `730`: CS2 App ID
- `2`: Context ID (in-game items)
- `count`: Items per page (max 5000)
- `start_assetid`: Pagination cursor (optional)

### Response Structure:
```json
{
  "assets": [
    {
      "appid": 730,
      "contextid": "2",
      "assetid": "123456789",
      "classid": "987654321",
      "instanceid": "0",
      "amount": "1"
    }
  ],
  "descriptions": [
    {
      "appid": 730,
      "classid": "987654321",
      "market_hash_name": "AK-47 | Slate (Field-Tested)",
      "name": "AK-47 | Slate",
      "type": "Rifle",
      "tradable": 1,
      "marketable": 1,
      "icon_url": "...",
      "descriptions": [
        {"value": "Exterior: Field-Tested"}
      ],
      "actions": [
        {
          "link": "steam://rungame/730/.../+csgo_econ_action_preview...",
          "name": "Inspect in Game..."
        }
      ]
    }
  ],
  "total_inventory_count": 150,
  "success": 1
}
```

### Python Implementation:
```python
import httpx
from typing import Dict List

async def get_steam_inventory(steam_id: str) -> Dict:
    """Fetch Steam CS2 inventory"""
    url = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
    params = {"count": 5000}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()

# Usage
inventory_data = await get_steam_inventory("76561198012345678")
print(f"Total items: {inventory_data['total_inventory_count']}")
```

### Pagination for Large Inventories (>5000 items):
```python
async def get_full_inventory(steam_id: str) -> List[Dict]:
    """Fetch all inventory items with pagination"""
    all_assets = []
    all_descriptions = []
    start_assetid = None
    
    while True:
        url = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
        params = {"count": 5000}
        
        if start_assetid:
            params["start_assetid"] = start_assetid
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            data = response.json()
        
        all_assets.extend(data.get("assets", []))
        all_descriptions.extend(data.get("descriptions", []))
        
        # Check if more items exist
        if not data.get("more_items"):
            break
        
        # Get last asset ID for next page
        start_assetid = data.get("last_assetid")
    
    return {
        "assets": all_assets,
        "descriptions": all_descriptions,
        "total_inventory_count": len(all_assets)
    }
```

---

## 5.4 Get Trade History

### Endpoint:
```
https://api.steampowered.com/IEconService/GetTradeHistory/v1/
```

### Parameters:
- `key`: Steam API key
- `max_trades`: Trades per request (max 500)
- `start_after_time`: Unix timestamp (pagination)
- `start_after_tradeid`: Trade ID (pagination)
- `get_descriptions`: 1 (include item details)
- `language`: en
- `include_failed`: 0
- `include_total`: 1

⚠️ **Note:** Requires user OAuth token (not just API key)

### Response Structure:
```json
{
  "response": {
    "trades": [
      {
        "tradeid": "123456789",
        "steamid_other": "76561198...",
        "time_init": 1707811200,
        "status": 3,
        "assets_received": [
          {
            "appid": 730,
            "contextid": "2",
            "assetid": "123456",
            "amount": "1",
            "classid": "987654"
          }
        ],
        "assets_given": []
      }
    ],
    "more": false,
    "total_trades": 150
  }
}
```

### Python Implementation:
```python
async def get_trade_history(api_key: str, max_trades: int = 100) -> Dict:
    """Fetch Steam trade history"""
    url = "https://api.steampowered.com/IEconService/GetTradeHistory/v1/"
    params = {
        "key": api_key,
        "max_trades": max_trades,
        "get_descriptions": 1,
        "language": "en",
        "include_failed": 0,
        "include_total": 1
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()
```

### Pagination for Full History (1 year):
```python
import asyncio
from datetime import datetime, timedelta

async def fetch_all_trades(api_key: str, days_back: int = 365) -> List[Dict]:
    """Fetch all trades from last X days"""
    all_trades = []
    start_time = int((datetime.now() - timedelta(days=days_back)).timestamp())
    
    while True:
        params = {
            "key": api_key,
            "max_trades": 500,
            "start_after_time": start_time,
            "get_descriptions": 1,
            "include_failed": 0
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.steampowered.com/IEconService/GetTradeHistory/v1/",
                params=params,
                timeout=30.0
            )
            data = response.json()
        
        trades = data["response"]["trades"]
        
        if not trades:
            break
        
        all_trades.extend(trades)
        
        # Update start time for next page
        start_time = trades[-1]["time_init"]
        
        # Check if more trades exist
        if not data["response"].get("more"):
            break
        
        # Rate limiting: wait 1 second between requests
        await asyncio.sleep(1)
    
    return all_trades

# Usage
trades = await fetch_all_trades("YOUR_API_KEY", days_back=365)
print(f"Fetched {len(trades)} trades")
```

---

## 5.5 Error Handling

### Common Steam API Errors:
```python
import httpx
from fastapi import HTTPException

async def safe_steam_api_call(url: str, params: dict) -> dict:
    """Make Steam API call with error handling"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            raise HTTPException(status_code=403, detail="Invalid Steam API key")
        elif e.response.status_code == 429:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        else:
            raise HTTPException(status_code=500, detail=f"Steam API error: {e}")
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Steam API timeout")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
```

---

## Next Steps

✅ **Lanjut ke:** [`06-CSFloat-Scraping.md`](06-CSFloat-Scraping.md) - Get real-time prices  
✅ **Alternative:** [`07-Rate-Limiting.md`](07-Rate-Limiting.md) - Implement rate limiter

---

**Steam API integrated! 🎮**
