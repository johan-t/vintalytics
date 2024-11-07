# Use Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the entire backend directory
COPY . /app/backend/

# Set the working directory to where we copied the backend
WORKDIR /app/backend

# Install dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache-dir -e .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]