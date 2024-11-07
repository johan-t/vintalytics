from urllib.parse import unquote
import pandas as pd
from collections import Counter
import re

# TODO: Add ai stuff to check if some keywords should stay together, like air force 1
def clean_title(title: str) -> list[str]:
    """Clean and tokenize title text"""
    # Convert to lowercase
    title = title.lower()
    
    # Remove specific patterns
    title = re.sub(r'\d+', '', title)         # Remove all numbers
    
    # Split into words and remove short words
    words = [word for word in re.findall(r'\w+', title) if len(word) > 2]
    
    # Remove common stop words (expand this list as needed)
    stop_words = {'the', 'and', 'for', 'with', 'neu', 'wie', 'von', 'aus', 'größe'}
    return [w for w in words if w not in stop_words]

def get_top_keywords(df: pd.DataFrame, brand: str, limit: int = 15) -> list[dict]:
    """Get top keywords from titles for a specific brand"""
    brand = unquote(brand)
    
    # Filter for brand
    brand_items = df[df['Brand'].str.lower() == brand.lower()]
    
    if brand_items.empty:
        return []
    
    # Process all titles
    all_words = []
    for title in brand_items['Title']:
        if isinstance(title, str):
            all_words.extend(clean_title(title))
    
    # Count frequencies
    word_counts = Counter(all_words)
    
    # Get top words
    top_words = word_counts.most_common(limit)
    return [{"word": word, "count": count} for word, count in top_words]

def get_keyword_price_analysis(df: pd.DataFrame, brand: str, keywords: list[str]) -> dict:
    """Analyze prices for items containing specific keywords"""
    brand = unquote(brand)
    keywords = [k.lower() for k in keywords]
    
    # Filter for brand
    brand_items = df[df['Brand'].str.lower() == brand.lower()]
    
    if brand_items.empty:
        return None
    
    # Filter for keywords
    mask = brand_items['Title'].str.lower().apply(
        lambda x: all(k in x for k in keywords) if isinstance(x, str) else False
    )
    matching_items = brand_items[mask]
    
    if matching_items.empty:
        return None
    
    return {
        "average_price": round(matching_items['Price'].mean(), 2),
        "count": len(matching_items),
        "min_price": round(matching_items['Price'].min(), 2),
        "max_price": round(matching_items['Price'].max(), 2)
    } 