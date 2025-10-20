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
    GET /boxes        - List all transport boxes
    GET /boxes/{id}   - Retrieve specific transport box details
    GET /samples      - List all biological samples
    GET /samples/{id} - Retrieve specific biological sample details
    GET /telemetry    - Fetch telemetry data with filtering options
    GET /sla          - List SLA configurations
    POST /sla         - Create new SLA configuration
    GET /alerts       - List alerts with filtering options

Dependencies:
    - FastAPI: Web framework and API documentation
    - aiosqlite: Async SQLite database operations
    - database.py: Database manager for Django DB access
    - analytics.py: Analytics utilities

"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("digital_twin_service")

app = FastAPI(
    title="Bio Supply Digital Twin Service",
    description="A service that simulates and analyzes digital twins of biological samples.",
    version="1.0.0",
)

# Enable CORS for local development (Vite dev server and Django backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database import DatabaseManager
from analytics import compute_compliance
from models import TransportBox as BoxModel, Sample as SampleModel, TelemetryReading, SLAConfig, Alert, Stats
from cache import cache

db = DatabaseManager()

@app.get("/")
async def root():
    """ Health check endpoint """
    return {
        "service": "Bio Supply Digital Twin Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """ Health check with simple cache status """
    cache_stats = cache.get_cache_stats()
    return {
        "status": "healthy",
        "service": "digital_twin", 
        "cache": cache_stats
    }


@app.get("/boxes", response_model=list[BoxModel])
async def list_boxes():
    """Get all transport boxes (no caching - for comparison)."""
    boxes = await db.get_all_boxes()
    return boxes


@app.get("/boxes/{box_id}", response_model=BoxModel)
async def get_box(box_id: str):
    """Get specific transport box (no caching)."""
    box = await db.get_box(box_id)
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")
    return box


@app.get("/samples", response_model=list[SampleModel])
async def list_samples():
    """Get all samples (no caching)."""
    samples = await db.get_all_samples()
    # Ensure schema compatibility: ids as strings
    for s in samples:
        if 'box_id' in s and s['box_id'] is not None:
            s['box_id'] = str(s['box_id'])
        if 'sample_id' in s and s['sample_id'] is not None:
            s['sample_id'] = str(s['sample_id'])
    return samples


@app.get("/samples/{sample_id}", response_model=SampleModel)
async def get_sample(sample_id: str):
    sample = await db.get_sample(sample_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    # Ensure schema compatibility
    if 'box_id' in sample and sample['box_id'] is not None:
        sample['box_id'] = str(sample['box_id'])
    if 'sample_id' in sample and sample['sample_id'] is not None:
        sample['sample_id'] = str(sample['sample_id'])
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
    """Get system statistics with caching."""
    # Try cache first
    cached_stats = cache.get_api_cache("stats")
    if cached_stats:
        cached_stats["from_cache"] = True
        return cached_stats
    
    # Cache miss - fetch from database
    num_boxes = await db.box_count()
    num_samples = await db.sample_count()
    num_active_alerts = await db.active_alert_count()
    
    stats = {
        "num_boxes": num_boxes, 
        "num_samples": num_samples, 
        "num_active_alerts": num_active_alerts,
        "from_cache": False
    }
    
    # Step 3: Store in cache for 30 seconds
    cache.set("stats", stats, ttl=30)
    return stats


@app.get("/analytics/compliance")
async def analytics_compliance(
    box: int | None = Query(None),
    sample: int | None = Query(None),
    since: str | None = Query(None),
    sla_name: str | None = Query(None, description="Optional SLA name; if omitted, use latest"),
):
    telemetry = await db.list_telemetry(
        box_id=box, sample_id=sample, since_iso=since
    )
    slas = await db.list_sla()
    if not slas:
        raise HTTPException(status_code=400, detail="No SLA configured")
    sla = None
    if sla_name:
        for s in slas:
            if s["name"] == sla_name:
                sla = s
                break
        if sla is None:
            raise HTTPException(status_code=404, detail="SLA not found")
    else:
        sla = slas[0]
    return compute_compliance(telemetry, sla)


# Simple Cache Endpoints
@app.get("/cache/stats")
async def get_cache_stats():
    """See basic cache information."""
    return cache.get_cache_stats()


@app.delete("/cache/clear")
async def clear_cache():
    """Clear the stats cache to see the difference."""
    deleted = cache.delete("stats")
    return {
        "message": "Cleared stats cache",
        "deleted": deleted
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)