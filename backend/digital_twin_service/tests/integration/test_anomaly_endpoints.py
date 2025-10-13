import pytest
import asyncio
from httpx import AsyncClient

# Optional HTTP client for integration tests
httpx = pytest.importorskip("httpx")
from digital_twin_service.main import app


@pytest.mark.asyncio
async def test_anomalies_endpoint_monkeypatched(monkeypatch):
    # Prepare synthetic telemetry
    telemetry = [
        {"timestamp": "2025-01-01T00:00:00Z", "temperature": 4.0, 
         "humidity": 50.0},
        {"timestamp": "2025-01-01T00:15:00Z", "temperature": 15.0, 
         "humidity": 50.0},  # anomaly
        {"timestamp": "2025-01-01T00:30:00Z", "temperature": 3.9, 
         "humidity": 49.0},
    ]

    async def fake_list_telemetry(box_id=None, sample_id=None, since_iso=None):
        return telemetry

    # Monkeypatch the db.list_telemetry method used by the app
    from digital_twin_service import main as main_mod
    monkeypatch.setattr(main_mod.db, 'list_telemetry', fake_list_telemetry)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/analytics/anomalies?algorithm=z_score")
        assert r.status_code == 200
        data = r.json()
        assert "anomalies" in data
        assert data["summary"]["total_points"] == len(telemetry)
        assert data["summary"]["anomalies_found"] >= 1


@pytest.mark.asyncio
async def test_temperature_endpoint(monkeypatch):
    telemetry = [
        {"timestamp": "2025-01-01T00:00:00Z", "temperature": 4.0},
        {"timestamp": "2025-01-01T00:15:00Z", "temperature": -10.0},
    ]

    async def fake_list_telemetry(box_id=None, sample_id=None, since_iso=None):
        return telemetry

    from digital_twin_service import main as main_mod
    monkeypatch.setattr(main_mod.db, 'list_telemetry', fake_list_telemetry)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/analytics/anomalies/temperature?algorithm=z_score")
        assert r.status_code == 200
        data = r.json()
        assert data["count"] >= 1
