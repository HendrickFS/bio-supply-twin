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

from fastapi import FastAPI, HTTPException, Query
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("digital_twin_service")

app = FastAPI(
    title="Bio Supply Digital Twin Service",
    description="A service that simulates and analyzes digital twins of biological samples.",
    version="1.0.0",
)

from .database import DatabaseManager
from .models import TransportBox as BoxModel, Sample as SampleModel, TelemetryReading, SLAConfig, Alert, Stats

db = DatabaseManager()

@app.get("/")
async def root():
    """ Health check endpoint """
    return {
        "service": "Bio Supply Digital Twin Service",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/boxes", response_model=list[BoxModel])
async def list_boxes():
    boxes = await db.get_all_boxes()
    return boxes


@app.get("/boxes/{box_id}", response_model=BoxModel)
async def get_box(box_id: str):
    box = await db.get_box(box_id)
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")
    return box


@app.get("/samples", response_model=list[SampleModel])
async def list_samples():
    samples = await db.get_all_samples()
    return samples


@app.get("/samples/{sample_id}", response_model=SampleModel)
async def get_sample(sample_id: str):
    sample = await db.get_sample(sample_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    return sample


@app.get("/telemetry", response_model=list[TelemetryReading])
async def list_telemetry(
    box: int | None = Query(None),
    sample: int | None = Query(None),
    since: str | None = Query(None, description="ISO timestamp lower bound"),
):
    return await db.list_telemetry(box_id=box, sample_id=sample, since_iso=since)


@app.get("/sla", response_model=list[SLAConfig])
async def list_sla():
    return await db.list_sla()


@app.post("/sla")
async def create_sla(payload: SLAConfig):
    ok = await db.create_sla(payload.name, payload.temp_min, payload.temp_max, payload.humidity_min, payload.humidity_max)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to create SLA")
    return {"created": True}


@app.get("/alerts", response_model=list[Alert])
async def list_alerts(active: bool = Query(False)):
    return await db.list_alerts(active_only=active)


@app.post("/alerts")
async def create_alert(payload: Alert):
    ok = await db.create_alert(payload.dict())
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to create alert")
    return {"created": True}


@app.get("/stats")
async def get_stats():
    num_boxes = await db.box_count()
    num_samples = await db.sample_count()
    num_active_alerts = await db.active_alert_count()
    return {"num_boxes": num_boxes, "num_samples": num_samples, "num_active_alerts": num_active_alerts}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)