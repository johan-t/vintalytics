from typing import Literal, Optional, List, Dict
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.modules.data_loader import load_data
from backend.modules.price_analysis import calculate_average_price
from backend.modules.listings_analysis import get_listings_by_timeframe
from backend.modules.keyword_analysis import (
    get_top_keywords,
    get_keyword_price_analysis,
)
from backend.modules.ai_price_analysis import ListingPriceAnalyzer

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Choose your data source

df = load_data()


@app.get("/")
async def root():
    return {"message": "Vintalytics API"}


@app.get("/api/brands")
async def get_brands() -> Dict[str, List[Dict[str, int | str]]]:
    # Get brand counts
    brand_counts = df["Brand"].value_counts()
    # Filter brands with at least certain number of entries
    qualified_brands = brand_counts[brand_counts >= 100]
    # Convert to list of dictionaries with brand and count
    brands_list = [
        {"brand": brand, "count": int(count)}
        for brand, count in qualified_brands.items()
    ]
    # Sort by count descending
    brands_list.sort(key=lambda x: x["count"], reverse=True)
    return {"brands": brands_list}


@app.get("/api/{brand_name}/{time_unit}/pricing/average")
async def get_average_price_timeframe(
    brand_name: str,
    time_unit: Literal["weekly", "monthly", "yearly"],
    start: Optional[str] = None,
    end: Optional[str] = None,
):
    try:
        # Validate dates if provided
        if start:
            datetime.strptime(start, "%Y-%m-%d")
        if end:
            datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )

    data = calculate_average_price(df, brand_name, time_unit, start, end)

    if not data:
        raise HTTPException(status_code=404, detail="No data found for brand")

    return {"brand": brand_name, "time_unit": time_unit, "data": data}


@app.get("/api/{brand_name}/{time_unit}/listings/count")
async def get_listings_timeframe(
    brand_name: str,
    time_unit: Literal["weekly", "monthly", "yearly"],
    start: Optional[str] = None,
    end: Optional[str] = None,
):
    try:
        # Validate dates if provided
        if start:
            datetime.strptime(start, "%Y-%m-%d")
        if end:
            datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )

    data = get_listings_by_timeframe(df, brand_name, time_unit, start, end)

    if not data:
        raise HTTPException(status_code=404, detail="No data found for brand")

    return {"brand": brand_name, "time_unit": time_unit, "data": data}


@app.get("/api/{brand_name}/keywords/top/{limit}")
async def get_brand_keywords(brand_name: str, limit: int):
    keywords = get_top_keywords(df, brand_name, limit)

    if not keywords:
        raise HTTPException(status_code=404, detail="Brand not found")

    return {"brand": brand_name, "keywords": keywords}


@app.get("/api/{brand_name}/keywords/{keywords}")
async def get_keyword_analysis(brand_name: str, keywords: str):
    # Split keywords by comma and clean
    keyword_list = [k.strip() for k in keywords.split(",")]

    analysis = get_keyword_price_analysis(df, brand_name, keyword_list)

    if analysis is None:
        raise HTTPException(
            status_code=404, detail="No items found matching all keywords"
        )

    return {"brand": brand_name, "keywords": keyword_list, "analysis": analysis}

# Add to FastAPI endpoints
@app.get("/api/ai/similar-listings/{keywords}")
async def get_similar_listings(keywords: str):
    keywords_list = keywords.split(',')
    analyzer = ListingPriceAnalyzer()
    analyzer.load_and_prepare_data(df)  # df from main.py
    
    results = analyzer.find_similar_listings(keywords_list)
    if not results:
        raise HTTPException(status_code=404, detail="No similar listings found")
        
    return {
        "keywords": keywords_list,
        "analysis": results
    }