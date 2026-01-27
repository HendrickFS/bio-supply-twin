## API Endpoints & Integration

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
