# Bio Supply Digital Twin

The Bio Supply Twin is a microservices-based Digital Twin that creates a living, data-driven replica of the biological sample supply chain. It combines a Django-powered Core Service for authoritative sample and container records with a FastAPI Digital Twin Service for real-time analytics and MQTT-driven telemetry ingestion.

## Architecture

**Core Service** (Django/DRF) - Sample and transport box management  
**Digital Twin Service** (FastAPI) - Real-time analytics and SLA compliance monitoring  
**MQTT Broker** (Mosquitto) - Telemetry data ingestion

## Quick Start

### With Docker (Recommended)
```bash
docker compose up --build
```

### Local Development
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Services

| Service | URL | Description |
|---------|-----|-------------|
| Core API | `http://localhost:8000` | Transport boxes, samples, telemetry |
| Digital Twin | `http://localhost:8001` | Analytics, SLA compliance |
| API Docs | `http://localhost:8001/docs` | Interactive FastAPI documentation |
| MQTT Broker | `mqtt://localhost:1883` | Telemetry ingestion |

## Key Features

- **Transport Box Management** - Track containers with location and environmental data
- **Sample Tracking** - Monitor biological samples throughout supply chain
- **SLA Compliance** - Real-time analytics against temperature/humidity thresholds
- **Excursion Detection** - Automatic alerts for threshold violations
- **MQTT Integration** - Real-time telemetry data ingestion

## API Overview

### Core Service (`localhost:8000`)
- `GET|POST /transport_boxes/` - Manage transport containers
- `GET|POST /samples/` - Track biological samples  
- `GET|POST /telemetry/` - Time-series sensor data
- `GET|POST /sla/` - SLA threshold configurations

### Digital Twin Service (`localhost:8001`)
- `GET /analytics/compliance` - SLA compliance analysis
- `GET /stats` - System overview metrics
- `GET /boxes, /samples` - Read-only data access



## Testing
```bash
pytest -q
```

## Development

### Run FastAPI Service Separately
```bash
pip install -r digital_twin_service/requirements.txt
uvicorn digital_twin_service.main:app --reload --port 8001
```

### MQTT Consumer
```bash
python manage.py mqtt_consumer
```

## Project Structure
```
├── core/                    # Django models, views, serializers
├── digital_twin_service/    # FastAPI analytics service
├── mosquitto/               # MQTT broker configuration
└── docker-compose.yml       # Service orchestration
```




