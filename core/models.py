"""
Bio Supply Core Service - Django Models
=======================================

Purpose:
    Django ORM models for biological supply chain management system.
    Defines database schema for transport boxes and biological samples
    with their sensor data and relationships.

Key Features:
    - TransportBox: Container tracking with environmental sensors
    - Sample: Biological specimen tracking with metadata
    - Foreign key relationships for data integrity
    - Automatic timestamp tracking for audit trails
    - Unique identifiers for external system integration

Database Schema:
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

Relationships:
    - One TransportBox can contain many Samples
    - Each Sample belongs to exactly one TransportBox

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

