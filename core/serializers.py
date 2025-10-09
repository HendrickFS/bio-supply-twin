"""
Bio Supply Core Service - DRF Serializers
========================================

Purpose:
    Serializers for converting model instances to/from JSON for API endpoints.

Includes:
    - TransportBoxSerializer, SampleSerializer
    - TelemetryReadingSerializer, SLAConfigSerializer, AlertSerializer

Data Flow:
    Model Instance -> Serializer -> JSON (responses)
    JSON Request -> Serializer -> Validated Data -> Model Instance

Dependencies:
    - Django REST Framework
    - core.models

"""

from rest_framework import serializers
from .models import TransportBox, Sample, TelemetryReading, SLAConfig, Alert



class TransportBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportBox
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'


class TelemetryReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryReading
        fields = '__all__'


class SLAConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SLAConfig
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'