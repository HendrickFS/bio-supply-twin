
"""
Bio Supply Digital Twin Service - Pydantic Models
================================================

Purpose:
    Pydantic data models for API request/response validation and serialization.
    Defines type-safe data structures for digital twin operations, analytics,
    and system monitoring in the biological supply chain system.

Key Features:
    - Type validation and automatic serialization via Pydantic
    - Data models for samples, transport boxes, and analytics results
    - Automatic JSON schema generation for FastAPI documentation
    - Data transformation methods from database records
    - Field validation with descriptive error messages

Models:
    - SampleState: Current state and metadata of biological samples
    - BoxState: Current state and sensor data of transport boxes
    - AnalyticsResult: Results from data analysis and anomaly detection
    - SystemStats: Overall system statistics and health metrics
    - EnvironmentalReading: Time-series environmental sensor data
    - Alert: System alerts and notifications for anomalies

API Integration:
    - Used as response_model in FastAPI endpoints
    - Provides automatic API documentation generation
    - Ensures type safety between database and API responses
    - Validates data structure integrity across services

Data Flow:
    Database Record -> Pydantic Model -> JSON API Response -> Frontend
    
Dependencies:
    - Pydantic: Data validation and serialization framework
    - FastAPI: Automatic integration for API documentation
    - Typing: Type hints for better code maintainability

"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class TransportBox(BaseModel):
    box_id: str = Field(..., description="Unique identifier from IoT system")
    geolocation: str = Field(..., description="GPS coordinates or location name")
    temperature: float = Field(..., description="Environmental temperature reading")
    humidity: float = Field(..., description="Environmental humidity reading")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Auto-updated timestamp")
    status: str = Field(..., description="Operational status (active, maintenance, etc.)")

    @classmethod
    def from_db_record(cls, record: Dict[str, Any]) -> 'TransportBox':
        return cls(
            box_id=record['box_id'],
            geolocation=record['geolocation'],
            temperature=record['temperature'],
            humidity=record['humidity'],
            last_updated=record['last_updated'],
            status=record['status']
        )

class Sample(BaseModel):
    sample_id: str = Field(..., description="Unique identifier from lab system")
    box_id: str = Field(..., description="Foreign key to TransportBox")
    name: str = Field(..., description="Sample name")
    description: str = Field(..., description="Sample description")
    collected_at: datetime = Field(..., description="Collection timestamp")
    status: str = Field(..., description="Sample status (collected, processed, stored, etc.)")
    temperature: float = Field(..., description="Sensor temperature reading at sample level")
    humidity: float = Field(..., description="Sensor humidity reading at sample level")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Auto-updated timestamp")

    @classmethod
    def from_db_record(cls, record: Dict[str, Any]) -> 'Sample':
        return cls(
            sample_id=record['sample_id'],
            box_id=record['box_id'],
            name=record['name'],
            description=record['description'],
            collected_at=record['collected_at'],
            status=record['status'],
            temperature=record['temperature'],
            humidity=record['humidity'],
            last_updated=record['last_updated']
        )