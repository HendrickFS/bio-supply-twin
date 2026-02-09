# Bio Supply Digital Twin

> **A sophisticated microservices-based Digital Twin system for biological sample supply chain management**

The Bio Supply Twin is a microservices-based Digital Twin that creates a living, data-driven replica of the biological sample supply chain. It combines a Django-powered Core Service for authoritative sample and container records with a FastAPI Digital Twin Service for real-time analytics and MQTT-driven telemetry ingestion. Built using modern technologies and industry best practices, such as **microservices design**, **real-time data processing**, **caching strategies**, and **containerized deployment**.

## Architecture & Technologies

### **Microservices Architecture**
- **Core Service** (Django/DRF) - Authoritative data management with RESTful APIs
- **Digital Twin Service** (FastAPI) - Real-time analytics with Redis caching
- **MQTT Broker** (Mosquitto) - IoT telemetry data ingestion
- **Redis Cache** - High-performance caching layer
- **PostgreSQL** - Robust relational database with ACID compliance

<img width="1145" height="273" alt="image" src="https://github.com/user-attachments/assets/8b0f86ce-3669-403e-8f53-46b9c533f92e" />

### **Key Technical Skills**
- **Performance Optimization** - Redis caching with TTL strategies
- **Real-time Systems** - MQTT pub/sub for IoT sensor data
- **DevOps & Containerization** - Docker Compose orchestration
- **Test-Driven Development** - Comprehensive test suite with pytest
- **Data Analytics** - SLA compliance monitoring and excursion detection
- **Database Design** - Normalized schema with foreign key relationships
- **API Design** - RESTful services with auto-generated documentation

## Quick Start

### **One-Command Deployment**
```bash
# Start all microservices (PostgreSQL, Redis, Django, FastAPI, MQTT)
docker compose up --build -d

# Verify all services are healthy
curl http://localhost:8001/health && echo "✅ Digital Twin Service"
curl http://localhost:8000/api/ && echo "✅ Core API Service"
```

## Service Architecture

| Service | URL | Technology Stack | Purpose |
|---------|-----|------------------|---------|
| **Core API** | `http://localhost:8000` | Django + DRF + PostgreSQL | CRUD operations, data persistence |
| **Digital Twin** | `http://localhost:8001` | FastAPI + Redis | Real-time analytics, caching |
| **Cache Layer** | `redis://localhost:6379` | Redis  | performance improvement |
| **Message Broker** | `mqtt://localhost:1883` | Mosquitto MQTT | IoT sensor data ingestion |
| **Database** | `postgresql://localhost:5432` | PostgreSQL | ACID-compliant data storage |

## Advanced Features

### **Real-Time IoT Integration**
- **MQTT Telemetry Ingestion** - Asynchronous sensor data processing
- **Environmental Monitoring** - Temperature/humidity tracking with GPS
- **Automated Alerting** - SLA violation detection and notifications
- **Digital Twin Analytics** - Real-time compliance monitoring

## API Endpoints & Integration

See [API_ENDPOINTS.md](API_ENDPOINTS.md) for detailed API documentation.

## Learning Outcomes

This project helped me to improve my skills in:

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
