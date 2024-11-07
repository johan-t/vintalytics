from urllib.parse import unquote
import pandas as pd
from collections import Counter
import re

def clean_text(text: str) -> list[str]:
    """Clean and tokenize text"""
    if not isinstance(text, str):
        return []
        
    # Convert to lowercase
    text = text.lower()
    
    # Remove specific patterns
    text = re.sub(r'\d+', '', text)
    
    # Split into words and remove short words
    words = [word for word in re.findall(r'\w+', text) if len(word) > 2]
    
    # Remove common stop words
    stop_words = {'the', 'and', 'for', 'with', 'neu', 'wie', 'von', 'aus', 'größe', 'mit'}
    return [w for w in words if w not in stop_words]

def get_top_keywords(df: pd.DataFrame, brand: str, limit: int = 15) -> list[dict]:
    """Get top keywords from all relevant columns for a specific brand"""
    brand = unquote(brand)
    
    # Filter for brand
    brand_items = df[df['Brand'].str.lower() == brand.lower()]
    
    if brand_items.empty:
        return []
    
    # Process all relevant columns
    all_words = []
    relevant_columns = ['Title', 'Categories', 'Colors', 'Materials', 'Styles']
    
    for _, row in brand_items[relevant_columns].iterrows():
        for col in relevant_columns:
            all_words.extend(clean_text(row[col]))
    
    # Count frequencies
    word_counts = Counter(all_words)
    
    # Get top words
    top_words = word_counts.most_common(limit)
    return [{"word": word, "count": count} for word, count in top_words]

def get_keyword_price_analysis(df: pd.DataFrame, brand: str, keywords: list[str]) -> dict:
    """Analyze prices for items containing specific keywords across all relevant columns"""
    brand = unquote(brand)
    keywords = [k.lower() for k in keywords]
    
    # Filter for brand
    brand_items = df[df['Brand'].str.lower() == brand.lower()]
    
    if brand_items.empty:
        return None
    
    # Combine all relevant columns for searching
    brand_items['combined_text'] = (
        brand_items['Title'].fillna('') + ' ' + 
        brand_items['Categories'].fillna('') + ' ' + 
        brand_items['Colors'].fillna('') + ' ' + 
        brand_items['Materials'].fillna('') + ' ' + 
        brand_items['Styles'].fillna('')
    ).str.lower()
    
    # Filter for keywords in combined text
    mask = brand_items['combined_text'].apply(
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