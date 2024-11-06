# Backend Setup

## Prerequisites

- Python 3.11 or higher
- uv (Python package manager)

## Installation

1. Install uv if you haven't already:
```bash
pip install uv
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

## Running the Server

(MAKE SURE YOU ARE CURRENTLY IN THE PARENT FOLDER OF backend SO WE CAN LOAD THE MODULES RIGHT)
Start the FastAPI server with:
```bash
uvicorn backend.main:app --reload
```

The server will be available at `http://localhost:8000`

## Available Endpoints

- `GET /`: Welcome message
- `GET /brands`: List of all unique brands in the dataset
- `GET /api/{brand-name}/pricing/average`: Get average price for a brand
- `GET /api/{brand-name}/{time-unit}/listings/count`: Get time-based listing counts
- `GET /api/{brand-name}/keywords/{keyword1},{keyword2}`: Get the average, min and max price and the count of found listings containing these keywords
- `GET /api/{brand-name}/keywords/top/{limit}`: Get the top `{limit}` keywords


### Time-based Listings Endpoint

The time-based listings endpoint supports:
- Time units: weekly, monthly, yearly
- Date range filtering with start and end dates
- ISO format dates (YYYY-MM-DD)

Example usage:
```bash
# Get monthly listings for H&M in 2024
curl "http://localhost:8000/api/H%26M/monthly/listings/count?start=2024-01-01&end=2024-12-31"

# Get weekly listings for Zara in Q1 2024
curl "http://localhost:8000/api/Zara/weekly/listings/count?start=2024-01-01&end=2024-03-31"

# Get yearly listings for Nike
curl "http://localhost:8000/api/Nike/yearly/listings/count"
```

Response format:
```json
{
    "brand": "H&M",
    "time_unit": "monthly",
    "data": [
        {"date": "2024-01-31", "count": 42},
        {"date": "2024-02-29", "count": 35},
        {"date": "2024-03-31", "count": 28}
    ]
}
```

### Keyword Analysis Endpoints

The keyword analysis endpoints allow you to:
1. Get the most common keywords in titles for a brand
2. Analyze prices for items containing specific keywords

#### Top Keywords Endpoint

Example usage:
```bash
# Get top 15 keywords for Nike
curl "http://localhost:8000/api/Nike/keywords/top/15"
```

Response format:
```json
{
    "brand": "Nike",
    "keywords": [
        {"word": "shirt", "count": 145},
        {"word": "jacket", "count": 89},
        {"word": "hoodie", "count": 67},
        {"word": "sneakers", "count": 54}
    ]
}
```

#### Keyword Price Analysis Endpoint

Example usage:
```bash
# Get price analysis for Nike items with "air" and "force" in the title
curl "http://localhost:8000/api/Nike/keywords/air,force"

# Get price analysis for H&M dresses
curl "http://localhost:8000/api/H%26M/keywords/dress"
```

Response format:
```json
{
    "brand": "Nike",
    "keywords": ["air", "force"],
    "analysis": {
        "average_price": 85.50,
        "count": 42,
        "min_price": 45.00,
        "max_price": 150.00
    }
}
```
