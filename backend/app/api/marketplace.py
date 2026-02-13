from fastapi import APIRouter, Query
from app.services.csplatform import CSPlatformService
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/compare/{item_name}")
async def compare_prices(
    item_name: str
):
    """
    Compare prices between Steam Market and 3rd party marketplace (CSFloat)
    
    Returns both prices for comparison
    """
    cs_platform = CSPlatformService()
    
    result = await cs_platform.get_dual_pricing(item_name)
    
    return result


@router.post("/bulk-compare")
async def bulk_compare_prices(
    item_names: List[str]
):
    """
    Get dual pricing for multiple items
    """
    cs_platform = CSPlatformService()
    
    results = []
    for item_name in item_names[:50]:  # Limit to 50 items
        price_data = await cs_platform.get_dual_pricing(item_name)
        results.append(price_data)
    
    return {
        "items": results,
        "total": len(results)
    }
