"""
Bio Supply Core Service - Django Models
=======================================

Purpose:
    Django ORM models for biological supply chain management system.
    Defines database schema for transport vehicles, transport boxes,
    samples, telemetry readings, SLA configurations, and alerts.

Key Features:
    - TransportBox: Container tracking with environmental sensors
    - Sample: Biological specimen tracking with metadata
    - Foreign key relationships for data integrity
    - Automatic timestamp tracking for audit trails
    - Unique identifiers for external system integration
    - Analytics/health fields for monitoring and alerting
    - Alert lifecycle management for excursions/anomalies
    - SLA configuration for temperature and humidity thresholds
    - Time-series telemetry for environmental monitoring
    - Data analysis and anomaly detection
    - System statistics and health metrics
    - Data freshness tracking

Database Schema:
    TransportVehicle:
        - vehicle_id: Unique identifier from IoT system
        - vehicle_type: Type of vehicle (car, plane, boat, etc.)
        - last_updated: Auto-updated timestamp
        - status: Operational status (active, maintenance, etc.)
    
    TransportBox:
        - box_id: Unique identifier from IoT system
        - geolocation: GPS coordinates or location name
        - temperature/humidity: Environmental sensor readings
        - status: Operational status (active, maintenance, etc.)
        - last_updated: Auto-updated timestamp

    Sample:
        - sample_id: Unique identifier from lab system
        - box: Foreign key to TransportBox (many-to-one)
        - name/description: Sample metadata
        - collected_at: Collection timestamp
        - temperature/humidity: Sensor readings at sample level
        - status: Sample status (collected, processed, stored, etc.)
        - last_updated: Auto-updated timestamp

    TelemetryReading:
        - box: Foreign key to TransportBox (many-to-one)
        - sample: Foreign key to Sample (many-to-one)
        - timestamp: Timestamp of the reading
        - temperature: Environmental temperature reading
        - humidity: Environmental humidity reading
        - geolocation: GPS coordinates or location name

    SLAConfig:
        - name: Unique identifier for the SLA config
        - temp_min: Minimum temperature
        - temp_max: Maximum temperature
        - humidity_min: Minimum humidity
        - humidity_max: Maximum humidity

    Alert:
        - box: Foreign key to TransportBox (many-to-one)
        - sample: Foreign key to Sample (many-to-one)
        - type: Type of alert (temperature_excursion, humidity_excursion, stale_data)
        - severity: Severity of the alert (info, warning, critical)
        - message: Message of the alert
        - started_at: Timestamp when the alert started

Relationships:
    - One TransportVehicle can contain many TransportBoxes
    - One TransportBox can contain many Samples
    - Each Sample belongs to exactly one TransportBox
    - Each TelemetryReading belongs to exactly one TransportBox or Sample
    - Each Alert belongs to exactly one TransportBox or Sample

"""

from django.db import models

class TransportBox(models.Model):
    box_id = models.CharField(max_length=100, unique=True)
    geolocation = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Box {self.box_id} - Geolocation: {self.geolocation}"
    
class Sample(models.Model):
    sample_id = models.CharField(max_length=100, unique=True)
    box = models.ForeignKey(TransportBox, related_name='samples', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    collected_at = models.DateTimeField()
    status = models.CharField(max_length=50)
    temperature = models.FloatField()
    humidity = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sample {self.sample_id} - Name: {self.name}"

# Telemetry time-series per box or sample (either relation can be set)
class TelemetryReading(models.Model):
    box = models.ForeignKey(TransportBox, related_name='telemetry', null=True, blank=True, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, related_name='telemetry', null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(db_index=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    geolocation = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["box", "timestamp"]),
            models.Index(fields=["sample", "timestamp"]),
        ]


# SLA/threshold configuration (global simple config for now)
class SLAConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    temp_min = models.FloatField(default=2.0)
    temp_max = models.FloatField(default=8.0)
    humidity_min = models.FloatField(default=30.0)
    humidity_max = models.FloatField(default=70.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SLA {self.name} (T:{self.temp_min}-{self.temp_max} H:{self.humidity_min}-{self.humidity_max})"


SEVERITY_CHOICES = (
    ("info", "Info"),
    ("warning", "Warning"),
    ("critical", "Critical"),
)


# Alert lifecycle for excursions/anomalies
class Alert(models.Model):
    box = models.ForeignKey(TransportBox, related_name='alerts', null=True, blank=True, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, related_name='alerts', null=True, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)  # e.g., temperature_excursion, humidity_excursion, stale_data
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="warning")
    message = models.TextField(blank=True, default="")
    started_at = models.DateTimeField(db_index=True)
    last_seen_at = models.DateTimeField(db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active", "severity"]),
            models.Index(fields=["box", "is_active"]),
            models.Index(fields=["sample", "is_active"]),
        ]

    def __str__(self):
        target = self.box.box_id if self.box else (self.sample.sample_id if self.sample else "global")
        return f"Alert[{self.severity}] {self.type} @ {target}"
