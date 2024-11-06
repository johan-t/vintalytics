from datetime import datetime
from typing import Literal, Optional
import pandas as pd
from urllib.parse import unquote

TimeUnit = Literal["weekly", "monthly", "yearly"]

def get_listings_by_timeframe(
    df: pd.DataFrame,
    brand: str,
    time_unit: TimeUnit,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> list[dict]:
    """
    Get listing counts grouped by time unit within a date range.
    Dates should be in ISO format: YYYY-MM-DD
    """
    brand = unquote(brand)
    
    # Filter for brand
    brand_items = df[df['Brand'].str.lower() == brand.lower()]
    
    if brand_items.empty:
        return []
    
    # Convert Item_Date to datetime
    brand_items['Item_Date'] = pd.to_datetime(brand_items['Item_Date'])
    
    # Apply date filters if provided
    if start_date:
        start = pd.to_datetime(start_date)
        brand_items = brand_items[brand_items['Item_Date'] >= start]
    if end_date:
        end = pd.to_datetime(end_date)
        brand_items = brand_items[brand_items['Item_Date'] <= end]
    
    # Group by time unit
    if time_unit == "weekly":
        grouped = brand_items.groupby(pd.Grouper(key='Item_Date', freq='W'))
    elif time_unit == "monthly":
        grouped = brand_items.groupby(pd.Grouper(key='Item_Date', freq='M'))
    else:  # yearly
        grouped = brand_items.groupby(pd.Grouper(key='Item_Date', freq='Y'))
    
    # Format results
    result = []
    for date, group in grouped:
        if not group.empty:
            result.append({
                "date": date.strftime("%Y-%m-%d"),
                "count": len(group)
            })
    
    return result