import httpx
import re
from typing import Dict, List, Optional
from app.config import settings
from urllib.parse import urlencode, parse_qs, urlparse
import logging

logger = logging.getLogger(__name__)


class SteamService:
    """Service for Steam API interactions"""
    
    def __init__(self):
        self.api_key = settings.steam_api_key
        self.base_url = settings.steam_web_api_url
        self.openid_url = "https://steamcommunity.com/openid/login"
    
    def get_login_url(self, return_url: str) -> str:
        """
        Generate Steam OpenID login URL
        
        Args:
            return_url: URL to redirect after login
            
        Returns:
            Steam login URL
        """
        params = {
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.mode": "checkid_setup",
            "openid.return_to": return_url,
            "openid.realm": return_url.rsplit('/', 1)[0],
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        }
        return f"{self.openid_url}?{urlencode(params)}"
    
    def verify_login(self, query_params: Dict) -> Optional[str]:
        """
        Verify Steam OpenID login response
        
        Args:
            query_params: Query parameters from Steam callback
            
        Returns:
            Steam ID if valid, None otherwise
        """
        # Change mode to check_authentication
        params = dict(query_params)
        params["openid.mode"] = "check_authentication"
        
        try:
            response = httpx.post(self.openid_url, data=params, timeout=10.0)
            if response.status_code == 200 and "is_valid:true" in response.text:
                # Extract Steam ID from claimed_id
                claimed_id = query_params.get("openid.claimed_id", "")
                match = re.search(r"https://steamcommunity.com/openid/id/(\d+)", claimed_id)
                if match:
                    return match.group(1)
        except Exception as e:
            logger.error(f"Steam login verification failed: {e}")
        
        return None
    
    async def get_player_summary(self, steam_id: str) -> Optional[Dict]:
        """
        Get player summary from Steam API
        
        Args:
            steam_id: 64-bit Steam ID
            
        Returns:
            Player data dict or None
        """
        url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v0002/"
        params = {
            "key": self.api_key,
            "steamids": steam_id
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                players = data.get("response", {}).get("players", [])
                if players:
                    return players[0]
        except Exception as e:
            logger.error(f"Failed to get player summary for {steam_id}: {e}")
        
        return None
    
    async def get_inventory(self, steam_id: str, app_id: int = 730, context_id: int = 2) -> Dict:
        """
        Get CS2 inventory for a Steam user
        
        Args:
            steam_id: 64-bit Steam ID
            app_id: Steam app ID (730 for CS2)
            context_id: Context ID (2 for in-game items)
            
        Returns:
            Dict with 'items' and 'total_value'
        """
        all_items = []
        start_assetid = None
        
        while True:
            url = f"https://steamcommunity.com/inventory/{steam_id}/{app_id}/{context_id}"
            params = {
                "count": 5000,
                "l": "english"
            }
            
            if start_assetid:
                params["start_assetid"] = start_assetid
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params, timeout=30.0)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Check if inventory is private
                    if "error" in data:
                        logger.error(f"Inventory error: {data['error']}")
                        return {"items": [], "error": data["error"]}
                    
                    # Get assets and descriptions
                    assets = data.get("assets", [])
                    descriptions = data.get("descriptions", [])
                    
                    # Create description lookup
                    desc_map = {
                        f"{d['classid']}_{d['instanceid']}": d 
                        for d in descriptions
                    }
                    
                    # Combine assets with descriptions
                    for asset in assets:
                        key = f"{asset['classid']}_{asset['instanceid']}"
                        desc = desc_map.get(key, {})
                        
                        item = {
                            "asset_id": asset["assetid"],
                            "name": desc.get("market_hash_name", "Unknown"),
                            "icon_url": desc.get("icon_url", ""),
                            "tradable": desc.get("tradable", 0) == 1,
                            "marketable": desc.get("marketable", 0) == 1,
                            "type": desc.get("type", ""),
                            "rarity": self._extract_rarity(desc.get("tags", [])),
                            "category": self._extract_category(desc.get("tags", [])),
                        }
                        
                        all_items.append(item)
                    
                    # Check if there are more items
                    if data.get("more_items", 0) == 1:
                        start_assetid = data.get("last_assetid")
                    else:
                        break
                        
            except httpx.HTTPError as e:
                logger.error(f"HTTP error fetching inventory: {e}")
                break
            except Exception as e:
                logger.error(f"Error fetching inventory: {e}")
                break
        
        return {
            "items": all_items,
            "total_items": len(all_items)
        }
    
    def _extract_rarity(self, tags: List[Dict]) -> Optional[str]:
        """Extract rarity from item tags"""
        for tag in tags:
            if tag.get("category") == "Rarity":
                return tag.get("localized_tag_name")
        return None
    
    def _extract_category(self, tags: List[Dict]) -> Optional[str]:
        """Extract category from item tags"""
        for tag in tags:
            if tag.get("category") == "Type":
                return tag.get("localized_tag_name")
        return None
    
    async def get_trade_history(self, steam_id: str, api_key: str) -> List[Dict]:
        """
        Get trade history for a Steam user
        
        Note: This requires Steam Web API key with trade history permission
        
        Args:
            steam_id: 64-bit Steam ID
            api_key: Steam API key
            
        Returns:
            List of trades
        """
        # Note: Steam doesn't provide a public API for trade history
        # This would require screen scraping or access to Steam's private APIs
        # For MVP, we'll return empty list
        logger.warning("Trade history API not yet implemented")
        return []
