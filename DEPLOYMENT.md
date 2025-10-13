# 🚀 Bio Supply Digital Twin - Deployment Guide

This guide provides comprehensive deployment and setup instructions for the Bio Supply Digital Twin system.

## 📋 Prerequisites

### **System Requirements**
- **Docker** and **Docker Compose** 
- **Node.js** for frontend development
- **Python** for local backend development

## 🐳 Production Deployment (Docker)

### **1. Clone and Setup**
```bash
# Clone the repository
git clone https://github.com/HendrickFS/bio-supply-twin.git
cd bio-supply-twin

# Copy environment configuration
cp .env.example .env
# Edit .env with your production values
```

### **2. Start All Services**
```bash
# Build and start all services
docker-compose up --build -d

# Check service health
docker-compose ps
docker-compose logs -f digital_twin
```

### **3. Verify Deployment**
```bash
# Test API endpoints
curl http://localhost:8001/health
curl http://localhost:8000/api/transport_boxes/

# Check Redis cache
curl http://localhost:8001/cache/stats

# View service logs
docker-compose logs django_core
docker-compose logs redis
```

### **4. Initialize Data**
```bash
# Apply database migrations
docker-compose exec django_core python manage.py migrate

# Create superuser (optional)
docker-compose exec django_core python manage.py createsuperuser

```

## 📊 Monitoring & Observability

### **Health Checks**
```bash
# Service health endpoints
curl http://localhost:8001/health        # Digital Twin service
curl http://localhost:8000/api/         # Django API
curl http://localhost:6379              # Redis (telnet)

# Cache performance metrics
curl http://localhost:8001/cache/stats
```
