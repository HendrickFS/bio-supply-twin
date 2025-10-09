"""
Bio Supply Core Service - Django REST Framework Serializers
==========================================================

Purpose:
    Django REST Framework serializers for converting model instances
    to/from JSON data. Handles data validation, transformation, and
    representation for API endpoints.

Key Features:
    - Model serialization for transport boxes and samples
    - Automatic field validation based on model constraints
    - JSON serialization/deserialization for API responses
    - Field-level and object-level validation support
    - Integration with Django model fields and relationships

Serializers:
    TransportBoxSerializer:
        - Serializes all TransportBox model fields
        - Handles box_id, geolocation, temperature, humidity, status
        - Automatic timestamp handling for last_updated

    SampleSerializer:
        - Serializes all Sample model fields
        - Handles sample_id, name, description, status, sensor data
        - Foreign key relationship to TransportBox
        - Datetime serialization for collected_at and last_updated

Data Flow:
    Model Instance -> Serializer -> JSON (for API responses)
    JSON Request -> Serializer -> Validated Data -> Model Instance

Dependencies:
    - Django REST Framework: Serialization framework
    - core.models: Database models to serialize

"""

from rest_framework import serializers
from .models import TransportBox, Sample

class TransportBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportBox
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'