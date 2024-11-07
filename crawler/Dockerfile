# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install curl and additional dependencies
RUN apt-get update && \
    apt-get install -y curl chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY vinted_cronjob.py .

# Create a directory for the output files
RUN mkdir /app/data

# Set volume for persistent storage
VOLUME /app/data

# Set environment variables
ENV CSV_OUTPUT_DIR=/app/data
ENV PYTHONUNBUFFERED=1

# Run the script
CMD ["python", "vinted_cronjob.py"]