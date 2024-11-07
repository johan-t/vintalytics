from urllib.parse import unquote
import pandas as pd

def calculate_average_price(df: pd.DataFrame, brand: str) -> float:
    """
    Calculate the average price for a specific brand.
    Returns None if brand not found or no valid prices.
    """
    # Clean brand name from URL encoding
    brand = unquote(brand)
    
    # Filter dataframe for the specific brand
    brand_items = df[df['Brand'].str.lower() == brand.lower()]
    
    if brand_items.empty:
        return None
    
    # Calculate average price
    average_price = brand_items['Price'].mean()
    return round(average_price, 2) 