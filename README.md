## Bio Supply Digital Twin - Project Documentation

### Project Description
The Bio Supply Twin is a microservices-based Digital Twin that creates a living, data-driven replica of the biological sample supply chain. It combines a Django-powered Core Service for authoritative sample and container records with a FastAPI Digital Twin Service for real-time analytics and MQTT-driven telemetry ingestion.

### Overview
This repository contains two cooperating services:
- **Django Core Service (`bio_supply_twin` / `core`)**: CRUD APIs for managing transport boxes and biological samples using Django REST Framework.
- **Digital Twin Service (`digital_twin_service`)**: A FastAPI-based service for analytics and MQTT-driven data ingestion.

A local Mosquitto broker is provided via Docker Compose for MQTT messaging.

### Repository Structure
```
bio_supply_dt/
  bio_supply_twin/      # Django project (settings, ASGI/WSGI, URLs)
  core/                 # Core Service (Django, MQTT Consumer)
  digital_twin_service/ # Digital Twin Service (FastAPI, Analytics)
  mosquitto/            # Mosquitto MQTT config
  docker-compose.yml    # Orchestrates services
  Dockerfile            # Django service container
```

### Domain Model (Core Service)
- `TransportBox`:
  - Fields: `box_id` (unique), `geolocation`, `temperature`, `humidity`, `status`, `last_updated` (auto)
- `Sample`:
  - Fields: `sample_id` (unique), `box` (FK to `TransportBox`), `name`, `description`, `collected_at`, `status`, `temperature`, `humidity`, `last_updated` (auto)

### API (Core Service)
Powered by Django REST Framework ViewSets with custom lookup fields:
- Transport boxes
  - List: `GET /transport_boxes/`
  - Detail: `GET /transport_boxes/{box_id}/`
  - Create: `POST /transport_boxes/`
  - Update: `PUT|PATCH /transport_boxes/{box_id}/`
  - Delete: `DELETE /transport_boxes/{box_id}/`
- Samples
  - List: `GET /samples/`
  - Detail: `GET /samples/{sample_id}/`
  - Create: `POST /samples/`
  - Update: `PUT|PATCH /samples/{sample_id}/`
  - Delete: `DELETE /samples/{sample_id}/`



### Local Development Setup
1) Python environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
pip install pytest pytest-django pytest-cov
```

2) Django DB and migrations
```bash
python manage.py migrate
python manage.py runserver
```

3) FastAPI service (optional, separate venv or reuse)
```bash
pip install -r digital_twin_service/requirements.txt
uvicorn digital_twin_service.main:app --reload --port 8001
```

### Running with Docker
Prerequisites: Docker Desktop.

Build and start services:
```bash
docker compose up --build
```

Services:
- Django API on `http://localhost:8000`
- FastAPI Digital Twin on `http://localhost:8001` (if configured in compose)
- Mosquitto MQTT broker on `mqtt://localhost:1883`

Stop:
```bash
docker compose down
```

### Testing (pytest)
We use `pytest` and `pytest-django` with module-level DB markers and shared fixtures.

Configuration: `pytest.ini`
```ini
[pytest]
DJANGO_SETTINGS_MODULE = bio_supply_twin.settings
python_files = tests.py test_*.py *_tests.py
testpaths = core
addopts = -ra
```

Run tests:
```bash
venv\Scripts\pytest -q
```

Fixtures: `core/conftest.py` provides `box` and `sample` ORM-backed fixtures.

Test suite:
- `core/tests/test_models.py`: model behavior (str, relations, uniqueness)
- `core/tests/test_serializers.py`: DRF serializers (serialize/validate/save)
- `core/tests/test_views.py`: DRF ViewSets (list/create/retrieve); custom lookup by `box_id`/`sample_id`

### MQTT & Digital Twin Notes
- `core/management/commands/mqtt_consumer.py`: management command for consuming MQTT messages and persisting to Django models.
- `digital_twin_service/`: FastAPI app, `analytics.py`, `database.py`, `models.py` support analytics and persistence.




