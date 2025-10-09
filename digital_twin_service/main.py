"""
Bio Supply Digital Twin Service - Main Application
==================================================

Purpose:
    FastAPI-based microservice for digital twin operations of biological samples
    and transport boxes. Provides real-time analytics, state management, and
    monitoring capabilities for the bio supply chain system.

Key Features:
    - RESTful API endpoints for sample and box data retrieval
    - Async database operations for performance
    - Auto-generated API documentation via FastAPI
    - Integration with Django backend database

Endpoints:
    GET /              - Health check and service info

Dependencies:
    - FastAPI: Web framework and API documentation
    - aiosqlite: Async SQLite database operations
    - database.py: Database manager for Django DB access

"""

from fastapi import FastAPI, HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("digital_twin_service")

app = FastAPI(
    title="Bio Supply Digital Twin Service",
    description="A service that simulates and analyzes digital twins of biological samples.",
    version="1.0.0",
)

@app.get("/")
async def root():
    """ Health check endpoint """
    return {
        "service": "Bio Supply Digital Twin Service",
        "status": "running",
        "version": "1.0.0"
    }