import httpx
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CSPlatformService:
    """Service for fetching prices from CS Platform (3rd party marketplace)"""
    
    def __init__(self):
        # CSFloat API (we'll use CSFloat as the 3rd party since CSPlatform might not exist)
        # You can replace with actual CSPlatform API if available
        self.base_url = "https://csfloat.com/api/v1"
        self.market_url = "https://csfloat.com/api/v1/listings"
    
    async def get_item_price(self, item_name: str) -> Optional[Dict]:
        """
        Get current market price from CSFloat (3rd party marketplace)
        
        Returns:
            Dict with 'price', 'source', 'currency' or None
        """
        try:
            # CSFloat uses market hash name
            params = {
                "market_hash_name": item_name,
                "sort_by": "lowest_price",
                "limit": 1
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.get(
                    self.market_url,
                    params=params,
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    logger.warning(f"CSFloat API returned {response.status_code}")
                    return None
                
                data = response.json()
                
                # Extract lowest price from listings
                if data and len(data) > 0:
                    listing = data[0]
                    price = listing.get("price", 0) / 100  # CSFloat prices are in cents
                    
                    return {
                        "price": price,
                        "source": "csfloat",
                        "currency": "USD"
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Error fetching CSFloat price for {item_name}: {e}")
            return None
    
    async def get_steam_market_price(self, item_name: str) -> Optional[Dict]:
        """
        Get current Steam Market price for comparison
        
        Returns:
            Dict with 'price', 'source', 'currency' or None
        """
        try:
            # Steam Community Market API
            url = f"https://steamcommunity.com/market/priceoverview/"
            params = {
                "appid": 730,  # CS2
                "currency": 1,  # USD
                "market_hash_name": item_name
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.get(
                    url,
                    params=params,
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    return None
                
                data = response.json()
                
                if data.get("success"):
                    # Parse price string like "$1.23"
                    price_str = data.get("lowest_price", "$0.00")
                    price = float(price_str.replace("$", "").replace(",", ""))
                    
                    return {
                        "price": price,
                        "source": "steam_market",
                        "currency": "USD"
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Error fetching Steam price for {item_name}: {e}")
            return None
    
    async def get_dual_pricing(self, item_name: str) -> Dict:
        """
        Get both Steam and 3rd party prices for comparison
        
        Returns:
            Dict with steam_price, third_party_price, best_price
        """
        # Fetch both prices concurrently
        steam_result = await self.get_steam_market_price(item_name)
        third_party_result = await self.get_item_price(item_name)
        
        steam_price = steam_result["price"] if steam_result else None
        third_party_price = third_party_result["price"] if third_party_result else None
        
        # Determine best price (lowest for buy, highest for sell)
        best_price = None
        best_source = None
        
        if steam_price and third_party_price:
            # For buying, lowest is best
            if third_party_price < steam_price:
                best_price = third_party_price
                best_source = "csfloat"
            else:
                best_price = steam_price
                best_source = "steam_market"
        elif steam_price:
            best_price = steam_price
            best_source = "steam_market"
        elif third_party_price:
            best_price = third_party_price
            best_source = "csfloat"
        
        return {
            "item_name": item_name,
            "steam_price": steam_price,
            "third_party_price": third_party_price,
            "best_price": best_price,
            "best_source": best_source,
            "currency": "USD"
        }
