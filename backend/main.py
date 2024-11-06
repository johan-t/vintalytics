from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.modules.data_loader import load_data
from backend.modules.price_analysis import calculate_average_price
from backend.modules.listings_analysis import get_listings_by_timeframe
from typing import Literal, Optional
from datetime import datetime

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data into memory
df = load_data()

@app.get("/")
async def root():
    return {"message": "Vintalytics API"}

@app.get("/brands")
async def get_brands():
    # Get unique brands and remove empty values
    brands = df['Brand'].dropna().unique().tolist()
    # Sort brands alphabetically
    brands.sort()
    return {"brands": brands}

@app.get("/api/{brand_name}/pricing/average")
async def get_average_price(brand_name: str):
    average_price = calculate_average_price(df, brand_name)
    
    if average_price is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    return {
        "brand": brand_name,
        "average_price": average_price,
        "currency": "EUR"  # Assuming all prices are in EUR based on your dataset
    }

@app.get("/api/{brand_name}/listings/count")
async def get_listings_count(brand_name: str):
    count = count_brand_listings(df, brand_name)
    
    if count == 0:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    return {
        "brand": brand_name,
        "count": count
    }

@app.get("/api/{brand_name}/{time_unit}/listings/count")
async def get_listings_timeframe(
    brand_name: str,
    time_unit: Literal["weekly", "monthly", "yearly"],
    start: Optional[str] = None,
    end: Optional[str] = None
):
    try:
        # Validate dates if provided
        if start:
            datetime.strptime(start, "%Y-%m-%d")
        if end:
            datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    data = get_listings_by_timeframe(
        df,
        brand_name,
        time_unit,
        start,
        end
    )
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found for brand")
    
    return {
        "brand": brand_name,
        "time_unit": time_unit,
        "data": data
    }