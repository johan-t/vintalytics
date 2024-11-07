from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from typing import List, Dict

class ListingPriceAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='german',
            min_df=1,
            ngram_range=(1, 3),
            max_features=5000
        )
        self.embeddings = None
        self.df = None
        
    def load_and_prepare_data(self, df: pd.DataFrame):
        """Load data and create TF-IDF vectors for all listings"""
        self.df = df.copy()
        
        # Clean price data
        self.df['Price'] = pd.to_numeric(self.df['Price'], errors='coerce')
        self.df = self.df.dropna(subset=['Price'])  # Remove rows with invalid prices
        
        # Combine relevant fields for text analysis
        self.df['combined_text'] = (
            self.df['Title'].fillna('') + ' ' + 
            self.df['Categories'].fillna('') + ' ' + 
            self.df['Colors'].fillna('') + ' ' + 
            self.df['Materials'].fillna('') + ' ' + 
            self.df['Styles'].fillna('')
        ).str.lower()
        
        # Create TF-IDF matrix
        print("Creating text vectors for listings...")
        self.embeddings = self.vectorizer.fit_transform(self.df['combined_text'])
        
    def find_similar_listings(self, keywords: List[str], threshold: float = 0.1) -> Dict:
        """Find similar listings based on keywords using TF-IDF and cosine similarity"""
        try:
            # Prepare keyword text
            keyword_text = ' '.join(keywords).lower()
            
            # Transform keywords using the same vectorizer
            keyword_vector = self.vectorizer.transform([keyword_text])
            
            # Calculate similarities using cosine similarity
            similarities = cosine_similarity(keyword_vector, self.embeddings)[0]
            
            # Dynamic threshold based on result count
            initial_matches = np.where(similarities >= threshold)[0]
            if len(initial_matches) < 20:  # If we have too few matches
                # Find top 20 matches regardless of threshold
                matching_indices = np.argsort(similarities)[-20:]
            else:
                matching_indices = initial_matches
            
            matching_listings = self.df.iloc[matching_indices]
            
            if matching_listings.empty:
                return None
            
            # Sort by similarity score
            similarity_scores = similarities[matching_indices]
            matching_listings = matching_listings.assign(similarity=similarity_scores)
            matching_listings = matching_listings.sort_values('similarity', ascending=False)
            
            # Added grouping by price ranges for better analysis
            price_ranges = pd.qcut(matching_listings['Price'], q=4)
            price_range_stats = matching_listings.groupby(price_ranges)['Price'].agg(['mean', 'count'])
            
            avg_price = matching_listings['Price'].mean()
            median_price = matching_listings['Price'].median()
            min_price = matching_listings['Price'].min()
            max_price = matching_listings['Price'].max()
            
            if not (np.isfinite(avg_price) and np.isfinite(median_price) and 
                   np.isfinite(min_price) and np.isfinite(max_price)):
                return None
            
            return {
                "average_price": round(float(avg_price), 2),
                "median_price": round(float(median_price), 2),
                "min_price": round(float(min_price), 2),
                "max_price": round(float(max_price), 2),
                "count": int(len(matching_listings)),
                "price_ranges": [
                    {
                        "range": f"{interval.left:.2f}-{interval.right:.2f}",
                        "count": int(stats['count']),
                        "average": round(float(stats['mean']), 2)
                    }
                    for interval, stats in price_range_stats.iterrows()
                ],
                "similar_items": [
                    {
                        "Title": str(item["Title"]),
                        "Price": round(float(item["Price"]), 2),
                        "Brand": str(item["Brand"]),
                        "similarity": round(float(item["similarity"]), 3)
                    }
                    for item in matching_listings[['Title', 'Price', 'Brand', 'similarity']]
                    .head(10)
                    .to_dict('records')
                    if np.isfinite(item["Price"])
                ]
            }
            
        except Exception as e:
            print(f"Error in find_similar_listings: {str(e)}")
            return None