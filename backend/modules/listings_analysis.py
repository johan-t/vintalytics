import pandas as pd
from urllib.parse import unquote

def count_brand_listings(df: pd.DataFrame, brand: str) -> int:
    """
    Count the number of listings for a specific brand.
    Returns 0 if brand not found.
    """
    # Clean brand name from URL encoding
    brand = unquote(brand)
    
    # Filter dataframe for the specific brand
    brand_items = df[df['Brand'].str.lower() == brand.lower()]
    
    return len(brand_items)