import httpx
from typing import Optional, Dict
import logging
from bs4 import BeautifulSoup
from app.models import PriceCache
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PriceService:
    """Service for fetching CS2 item prices"""
    
    def __init__(self):
        # CSFloat market API (public, no auth needed)
        self.csfloat_api_url = "https://csfloat.com/api/v1/listings"
        self.steam_market_url = "https://steamcommunity.com/market/priceoverview/"
        self.cache_ttl = 300  # 5 minutes cache
    
    async def get_item_price(self, item_name: str, db: Session = None) -> Optional[float]:
        """
        Get price for an item, with caching
        
        Args:
            item_name: Market hash name of the item
            db: Database session for caching
            
        Returns:
            Price in USD or None
        """
        # Check cache first
        if db:
            cached_price = self._get_cached_price(item_name, db)
            if cached_price is not None:
                logger.debug(f"Using cached price for {item_name}: ${cached_price}")
                return cached_price
        
        # Try CSFloat first (more accurate for CS2 items)
        price = await self._get_csfloat_price(item_name)
        
        # Fallback to Steam Market
        if price is None:
            price = await self._get_steam_market_price(item_name)
        
        # Cache the price
        if price is not None and db:
            self._cache_price(item_name, price, db)
        
        return price
    
    async def _get_csfloat_price(self, item_name: str) -> Optional[float]:
        """
        Get price from CSFloat market
        
        CSFloat API is public and doesn't require auth for basic price checks
        """
        try:
            # CSFloat API endpoint for listings
            params = {
                "market_hash_name": item_name,
                "limit": 10,
                "sort_by": "lowest_price"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.csfloat_api_url,
                    params=params,
                    timeout=10.0,
                    headers={"User-Agent": "CS2Tracker/1.0"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Get listings
                    listings = data.get("data", [])
                    
                    if listings:
                        # Get average of lowest 3 prices
                        prices = [
                            listing.get("price", 0) / 100  # CSFloat uses cents
                            for listing in listings[:3]
                            if listing.get("price")
                        ]
                        
                        if prices:
                            avg_price = sum(prices) / len(prices)
                            logger.info(f"CSFloat price for {item_name}: ${avg_price:.2f}")
                            return round(avg_price, 2)
                
        except Exception as e:
            logger.warning(f"Failed to get CSFloat price for {item_name}: {e}")
        
        return None
    
    async def _get_steam_market_price(self, item_name: str) -> Optional[float]:
        """
        Fallback: Get price from Steam Community Market
        
        Note: Steam has rate limits, use sparingly
        """
        try:
            params = {
                "appid": 730,  # CS2
                "currency": 1,  # USD
                "market_hash_name": item_name
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.steam_market_url,
                    params=params,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Steam returns prices as strings like "$1.23"
                    lowest_price = data.get("lowest_price", "")
                    median_price = data.get("median_price", "")
                    
                    # Parse price (remove $ and convert to float)
                    price_str = lowest_price or median_price
                    if price_str:
                        price = float(price_str.replace("$", "").replace(",", ""))
                        logger.info(f"Steam Market price for {item_name}: ${price:.2f}")
                        return round(price, 2)
                
        except Exception as e:
            logger.warning(f"Failed to get Steam Market price for {item_name}: {e}")
        
        return None
    
    def _get_cached_price(self, item_name: str, db: Session) -> Optional[float]:
        """Get cached price if still fresh"""
        try:
            cache_entry = db.query(PriceCache).filter(
                PriceCache.item_name == item_name
            ).first()
            
            if cache_entry:
                # Check if cache is still fresh (within TTL)
                age = datetime.utcnow() - cache_entry.cached_at
                if age.total_seconds() < self.cache_ttl:
                    return cache_entry.price
        except Exception as e:
            logger.error(f"Error reading price cache: {e}")
        
        return None
    
    def _cache_price(self, item_name: str, price: float, db: Session):
        """Cache price in database"""
        try:
            # Check if entry exists
            cache_entry = db.query(PriceCache).filter(
                PriceCache.item_name == item_name
            ).first()
            
            if cache_entry:
                # Update existing
                cache_entry.price = price
                cache_entry.cached_at = datetime.utcnow()
            else:
                # Create new
                cache_entry = PriceCache(
                    item_name=item_name,
                    price=price,
                    cached_at=datetime.utcnow()
                )
                db.add(cache_entry)
            
            db.commit()
            logger.debug(f"Cached price for {item_name}: ${price}")
            
        except Exception as e:
            logger.error(f"Error caching price: {e}")
            db.rollback()
    
    async def bulk_fetch_prices(self, item_names: list, db: Session = None) -> Dict[str, float]:
        """
        Fetch prices for multiple items
        
        Args:
            item_names: List of item names
            db: Database session for caching
            
        Returns:
            Dict mapping item name to price
        """
        prices = {}
        
        # Fetch prices with a small delay to avoid rate limits
        import asyncio
        
        for item_name in item_names:
            price = await self.get_item_price(item_name, db)
            if price:
                prices[item_name] = price
            
            # Small delay to be nice to APIs
            await asyncio.sleep(0.5)
        
        return prices
