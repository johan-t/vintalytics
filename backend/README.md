
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
- `GET /api/{brand-name}/listings/count`: Get total number of listings for a brand
- `GET /api/{brand-name}/{time-unit}/listings/count`: Get time-based listing counts

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
