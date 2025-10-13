# 🧬 Bio Supply Digital Twin

> **A sophisticated microservices-based Digital Twin system for biological sample supply chain management**

The Bio Supply Twin is a microservices-based Digital Twin that creates a living, data-driven replica of the biological sample supply chain. It combines a Django-powered Core Service for authoritative sample and container records with a FastAPI Digital Twin Service for real-time analytics and MQTT-driven telemetry ingestion. Built using modern technologies and industry best practices, such as **microservices design**, **real-time data processing**, **caching strategies**, and **containerized deployment**.

## 🏗️ Architecture & Technologies

### **Microservices Architecture**
- **Core Service** (Django/DRF) - Authoritative data management with RESTful APIs
- **Digital Twin Service** (FastAPI) - Real-time analytics with Redis caching
- **MQTT Broker** (Mosquitto) - IoT telemetry data ingestion
- **Redis Cache** - High-performance caching layer
- **PostgreSQL** - Robust relational database with ACID compliance

### **Key Technical Skills Demonstrated**
- ⚡ **Performance Optimization** - Redis caching with TTL strategies
- 🔄 **Real-time Systems** - MQTT pub/sub for IoT sensor data
- 🐳 **DevOps & Containerization** - Docker Compose orchestration
- 🧪 **Test-Driven Development** - Comprehensive test suite with pytest
- 📊 **Data Analytics** - SLA compliance monitoring and excursion detection
- 🔐 **Database Design** - Normalized schema with foreign key relationships
- 🌐 **API Design** - RESTful services with auto-generated documentation

## 🚀 Quick Start

### **🐳 One-Command Deployment**
```bash
# Start all microservices (PostgreSQL, Redis, Django, FastAPI, MQTT)
docker compose up --build -d

# Verify all services are healthy
curl http://localhost:8001/health && echo "✅ Digital Twin Service"
curl http://localhost:8000/api/ && echo "✅ Core API Service"
```
Check out the [DEPLOYMENT.md](./DEPLOYMENT.md) for a complete production deployment guide.


## 🌐 Service Architecture

| Service | URL | Technology Stack | Purpose |
|---------|-----|------------------|---------|
| **Core API** | `http://localhost:8000` | Django + DRF + PostgreSQL | CRUD operations, data persistence |
| **Digital Twin** | `http://localhost:8001` | FastAPI + Redis | Real-time analytics, caching |
| **Cache Layer** | `redis://localhost:6379` | Redis  | performance improvement |
| **Message Broker** | `mqtt://localhost:1883` | Mosquitto MQTT | IoT sensor data ingestion |
| **Database** | `postgresql://localhost:5432` | PostgreSQL | ACID-compliant data storage |

## ✨ Advanced Features

### **Real-Time IoT Integration**
- 📡 **MQTT Telemetry Ingestion** - Asynchronous sensor data processing
- 🌡️ **Environmental Monitoring** - Temperature/humidity tracking with GPS
- ⚠️ **Automated Alerting** - SLA violation detection and notifications
- 📊 **Digital Twin Analytics** - Real-time compliance monitoring


## 🔌 API Endpoints & Integration

### **Core Service** - Django REST Framework (`localhost:8000`)
```python
# CRUD Operations with Django ORM
GET|POST   /api/transport_boxes/     # Container management
GET|POST   /api/samples/            # Biological sample tracking  
GET|POST   /api/telemetry/          # Time-series sensor data
GET|POST   /api/sla/               # SLA threshold configuration
GET|POST   /api/alerts/             # Alert management system
```

### **Digital Twin Service** - FastAPI with Caching (`localhost:8001`)
```python
# High-Performance Analytics with Redis Caching
GET  /stats                    # System metrics (cached 30s)
GET  /boxes/{box_id}          # Specific container data
GET  /analytics/compliance    # SLA compliance analysis
GET  /telemetry              # Filtered telemetry queries
GET  /health                 # Service health + cache status

# Cache Management (Learning/Debugging)
GET     /cache/stats         # Cache performance metrics
DELETE  /cache/clear         # Cache invalidation
```

### **MQTT Integration** - IoT Sensor Data (`localhost:1883`)
```bash
# Real-time telemetry ingestion
Topic: bio_supply/updates/box/{BOX_ID}
Topic: bio_supply/updates/sample/{SAMPLE_ID}

# Payload format:
{
  "temperature": 4.2,
  "humidity": 55.0,
  "timestamp": "2025-10-13T10:30:00Z",
  "geolocation": "52.5200,13.4050"
}
```

## 📁 Project Architecture & Structure

```
bio-supply-twin/
├── 🐳 docker-compose.yml           # Multi-service orchestration
├── 📊 backend/
│   ├── 🌐 core/                    # Django REST API Service
│   │   ├── models.py              # Data models with relationships
│   │   ├── serializers.py         # DRF serialization
│   │   ├── views.py               # RESTful API endpoints  
│   │   ├── tests/                 # Comprehensive test suite
│   │   └── management/commands/   # MQTT consumer command
│   ├── ⚡ digital_twin_service/   # FastAPI Analytics Service
│   │   ├── main.py               # FastAPI app with caching
│   │   ├── cache.py              # Redis cache manager
│   │   ├── database.py           # Async database operations
│   │   ├── analytics.py          # SLA compliance algorithms
│   │   ├── models.py             # Pydantic data models
│   │   └── tests/                # Unit & integration tests
│   ├── 🗃️ mosquitto/             # MQTT Broker Configuration
│   └── 📋 requirements.txt       # Python dependencies
├── 🎛️ frontend/                   # React TypeScript UI (Future)
├── 🧪 scripts/                    # Development & testing tools
│   ├── cache_test.py             # Redis performance demo
│   └── data_generator.py         # IoT data simulation
├── 🔄 .github/workflows/         # CI/CD Pipeline
│   ├── backend-ci.yml            # Automated testing
│   └── frontend-ci.yml           # Build verification
├── 📚 README.md                   # This documentation  
└── 🚀 DEPLOYMENT.md               # Complete deployment guide
```

## 🎯 Technical Skills Showcased

### **Backend Engineering**
- **Python** - Django, FastAPI, async/await patterns
- **Database Design** - PostgreSQL, migrations, relationships
- **API Development** - RESTful design, OpenAPI documentation
- **Caching Strategies** - Redis TTL, cache invalidation patterns
- **Message Queues** - MQTT pub/sub, real-time processing

### **DevOps & Infrastructure**
- **Containerization** - Docker, multi-service orchestration
- **Service Architecture** - Microservices, health checks, networking
- **Performance Optimization** - Caching, async operations, database indexing
- **Monitoring** - Health endpoints, cache metrics, system stats

### **Software Engineering Practices**
- **Testing** - Unit tests, integration tests, mocking
- **Code Quality** - Type hints, linting, documentation
- **Version Control** - Git workflows, CI/CD pipelines
- **Documentation** - Technical writing, API documentation


**Technologies:** Python • Django • FastAPI • PostgreSQL • Redis • MQTT • Docker • pytest • CI/CD

---

*Built by [Hendrick](https://github.com/HendrickFS) - Showcasing full-stack development and systems architecture skills*