from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import glob
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load and process data at startup
def load_data():
    # Get all CSV files from dataset folder
    csv_files = glob.glob("backend/dataset/*.csv")
    
    # Create empty list to store dataframes
    dfs = []
    
    # Read each CSV file and append to list
    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)
    
    # Concatenate all dataframes
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        # Remove duplicates based on all columns
        combined_df = combined_df.drop_duplicates()
        return combined_df
    return pd.DataFrame()

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