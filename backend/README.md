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

## Testing the API

Test the brands endpoint with:
```bash
curl http://localhost:8000/brands
```
