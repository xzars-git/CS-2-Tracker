import httpx
from typing import Dict, List, Optional
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class SteamMarketService:
    """Service for fetching Steam Market transaction history"""
    
    def __init__(self):
        self.market_history_url = "https://steamcommunity.com/market/myhistory"
        self.render_url = "https://steamcommunity.com/market/myhistory/render/"
    
    async def fetch_market_history(
        self, 
        cookies: str,
        count: int = 500
    ) -> Dict:
        """
        Fetch Steam Market transaction history using browser cookies
        
        Args:
            cookies: Browser cookies string (format: "name1=value1; name2=value2")
            count: Number of transactions to fetch (max 500 per request)
            
        Returns:
            Dict with 'success', 'transactions', and 'total_count'
        """
        try:
            # Parse cookies string into dict
            cookie_dict = self._parse_cookies(cookies)
            
            if not cookie_dict:
                return {
                    "success": False,
                    "error": "Invalid cookies format",
                    "transactions": []
                }
            
            # Fetch market history
            transactions = []
            start = 0
            
            while start < count:
                batch = await self._fetch_batch(
                    cookie_dict,
                    start=start,
                    count=min(100, count - start)  # Steam limits to 100 per call
                )
                
                if not batch["success"]:
                    break
                
                batch_transactions = batch.get("transactions", [])
                if not batch_transactions:
                    break
                
                transactions.extend(batch_transactions)
                start += len(batch_transactions)
                
                # If we got less than requested, we're done
                if len(batch_transactions) < 100:
                    break
            
            logger.info(f"Fetched {len(transactions)} market transactions")
            
            return {
                "success": True,
                "transactions": transactions,
                "total_count": len(transactions)
            }
            
        except Exception as e:
            logger.error(f"Error fetching market history: {e}")
            return {
                "success": False,
                "error": str(e),
                "transactions": []
            }
    
    async def _fetch_batch(
        self,
        cookies: Dict,
        start: int = 0,
        count: int = 100
    ) -> Dict:
        """
        Fetch a batch of market transactions
        
        Args:
            cookies: Cookie dict
            start: Start index
            count: Number of items to fetch
            
        Returns:
            Dict with success status and transactions
        """
        params = {
            "count": count,
            "start": start
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://steamcommunity.com/market/",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        try:
            async with httpx.AsyncClient(cookies=cookies, headers=headers) as client:
                response = await client.get(
                    self.render_url,
                    params=params,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    logger.error(f"HTTP {response.status_code} from Steam market")
                    return {"success": False, "transactions": []}
                
                data = response.json()
                
                if not data.get("success"):
                    logger.error(f"Steam API error: {data.get('error', 'Unknown')}")
                    return {"success": False, "transactions": []}
                
                # Parse HTML to extract transactions
                transactions = self._parse_market_html(data.get("results_html", ""))
                
                return {
                    "success": True,
                    "transactions": transactions,
                    "total_count": data.get("total_count", 0)
                }
                
        except Exception as e:
            logger.error(f"Error in _fetch_batch: {e}")
            return {"success": False, "transactions": []}
    
    def _parse_market_html(self, html: str) -> List[Dict]:
        """
        Parse Steam market history HTML to extract transactions
        
        This is a simplified parser - you might need to adjust based on actual HTML structure
        """
        from bs4 import BeautifulSoup
        
        transactions = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find all market history rows
            rows = soup.find_all('div', class_='market_listing_row')
            
            for row in rows:
                try:
                    # Extract item name
                    name_elem = row.find('span', class_='market_listing_item_name')
                    item_name = name_elem.text.strip() if name_elem else "Unknown"
                    
                    # Extract price
                    price_elem = row.find('span', class_='market_listing_price')
                    price_text = price_elem.text.strip() if price_elem else "$0.00"
                    price = self._parse_price(price_text)
                    
                    # Extract date
                    date_elem = row.find('div', class_='market_listing_listed_date')
                    date_text = date_elem.text.strip() if date_elem else ""
                    timestamp = self._parse_date(date_text)
                    
                    # Determine if it's a buy or sell
                    # (Steam shows "+" for bought, "-" for sold in the gain/loss column)
                    gain_elem = row.find('div', class_='market_listing_gainorloss')
                    is_purchase = True
                    if gain_elem:
                        gain_text = gain_elem.text.strip()
                        is_purchase = not gain_text.startswith('-')
                    
                    transaction = {
                        "item_name": item_name,
                        "price": price,
                        "trade_type": "BUY" if is_purchase else "SELL",
                        "timestamp": timestamp,
                        "source": "steam_market"
                    }
                    
                    transactions.append(transaction)
                    
                except Exception as e:
                    logger.warning(f"Error parsing transaction row: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error parsing market HTML: {e}")
        
        return transactions
    
    def _parse_cookies(self, cookie_string: str) -> Dict:
        """
        Parse cookie string into dictionary
        
        Format: "name1=value1; name2=value2; name3=value3"
        """
        cookies = {}
        
        try:
            for item in cookie_string.split(';'):
                item = item.strip()
                if '=' in item:
                    name, value = item.split('=', 1)
                    cookies[name.strip()] = value.strip()
        except Exception as e:
            logger.error(f"Error parsing cookies: {e}")
        
        return cookies
    
    def _parse_price(self, price_text: str) -> float:
        """
        Parse price string to float
        
        Examples: "$1.23", "Rp 15,000", "€2.50"
        """
        try:
            # Remove currency symbols and commas
            cleaned = price_text.replace('$', '').replace('€', '').replace('£', '')
            cleaned = cleaned.replace('Rp', '').replace(',', '').strip()
            
            return float(cleaned)
        except:
            return 0.0
    
    def _parse_date(self, date_text: str) -> datetime:
        """
        Parse Steam date format to datetime
        
        Examples: "13 Feb", "13 Feb, 2026"
        """
        try:
            # Steam uses format like "13 Feb" or "13 Feb @ 4:39pm"
            # For simplicity, use current year if year not specified
            from dateutil import parser
            
            # Try to parse with dateutil
            dt = parser.parse(date_text, fuzzy=True)
            return dt
            
        except:
            # Fallback to current datetime
            return datetime.utcnow()
