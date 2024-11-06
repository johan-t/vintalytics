from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.modules.data_loader import load_data
from backend.modules.price_analysis import calculate_average_price
from backend.modules.listings_analysis import count_brand_listings

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