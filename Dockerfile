# Use Python 3.10-slim as the base image and specify the platform
FROM --platform=linux/amd64 python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    build-essential \
    wget \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Upgrade pip and install setuptools and wheel
RUN pip install --upgrade pip setuptools wheel

# Install sqlite-vec separately
RUN pip install sqlite-vec

# Install other Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Define environment variables (optional)
ENV DATA_FOLDER=/app/data/example_data
ENV DB_FILE=/app/documents.db

# Define the command to run your application
CMD ["python", "main.py"]