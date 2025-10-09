# Bio Supply Digital Twin Service - Dockerfile
# ============================================
#
# Purpose:
#     Docker container configuration for the FastAPI-based digital twin
#     microservice. Creates a lightweight Python environment optimized
#     for API operations and database connectivity.
#
# Base Image: python:3.11-slim (lightweight Python runtime)
# Exposed Port: 8001 (FastAPI application server)
# Working Directory: /app
#
# Build Command: docker build -t digital-twin-service .
# Run Command: docker run -p 8001:8001 digital-twin-service

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Note: EXPOSE, HEALTHCHECK, and CMD are handled by docker-compose.yml
# This keeps the Dockerfile focused on image building, while docker-compose
# handles runtime configuration, service orchestration, and deployment settings
