"""
Bio Supply Core Service - Django REST API Views
==============================================

Purpose:
    Django REST Framework ViewSets for biological supply chain API endpoints.
    Provides CRUD operations for transport vehicles, transport boxes, samples, telemetry readings,
    SLA configurations, and alerts with RESTful API interface for external systems and frontend applications.

Key Features:
    - ModelViewSet for full CRUD operations (Create, Read, Update, Delete)
    - Custom lookup fields for external system integration
    - Automatic serialization/deserialization of model data
    - HTTP methods mapping: GET, POST, PUT, PATCH, DELETE
    - Pagination and filtering support via DRF

API Endpoints:
    TransportBox ViewSet:
        - GET /api/boxes/: List all transport boxes
        - GET /api/boxes/{box_id}/: Retrieve specific box
        - POST /api/boxes/: Create new transport box
        - PUT/PATCH /api/boxes/{box_id}/: Update transport box
        - DELETE /api/boxes/{box_id}/: Delete transport box

    Sample ViewSet:
        - GET /api/samples/: List all samples
        - GET /api/samples/{sample_id}/: Retrieve specific sample
        - POST /api/samples/: Create new sample
        - PUT/PATCH /api/samples/{sample_id}/: Update sample
        - DELETE /api/samples/{sample_id}/: Delete sample

    TelemetryReading ViewSet:
        - GET /api/telemetry/: List all telemetry readings
        - GET /api/telemetry/{telemetry_id}/: Retrieve specific telemetry reading
        - POST /api/telemetry/: Create new telemetry reading
        - PUT/PATCH /api/telemetry/{telemetry_id}/: Update telemetry reading
        - DELETE /api/telemetry/{telemetry_id}/: Delete telemetry reading

    SLAConfig ViewSet:
        - GET /api/sla/: List all SLA configurations
        - GET /api/sla/{sla_id}/: Retrieve specific SLA configuration
        - POST /api/sla/: Create new SLA configuration
        - PUT/PATCH /api/sla/{sla_id}/: Update SLA configuration
        - DELETE /api/sla/{sla_id}/: Delete SLA configuration

    Alert ViewSet:
        - GET /api/alerts/: List all alerts
        - GET /api/alerts/{alert_id}/: Retrieve specific alert
        - POST /api/alerts/: Create new alert
        - PUT/PATCH /api/alerts/{alert_id}/: Update alert
        - DELETE /api/alerts/{alert_id}/: Delete alert

Lookup Fields:
    - TransportBox: Uses 'box_id' instead of default 'id'
    - Sample: Uses 'sample_id' instead of default 'id'

Dependencies:
    - Django REST Framework: API framework
    - core.models: Database models
    - core.serializers: Data serialization

"""

from django.shortcuts import render
from rest_framework import viewsets
from .models import TransportBox, Sample, TelemetryReading, SLAConfig, Alert
from .serializers import (
    TransportBoxSerializer,
    SampleSerializer,
    TelemetryReadingSerializer,
    SLAConfigSerializer,
    AlertSerializer,
)


class TransportBoxViewSet(viewsets.ModelViewSet):
    queryset = TransportBox.objects.all()
    serializer_class = TransportBoxSerializer
    lookup_field = 'box_id'

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    lookup_field = 'sample_id'


class TelemetryReadingViewSet(viewsets.ModelViewSet):
    queryset = TelemetryReading.objects.all().order_by('-timestamp')
    serializer_class = TelemetryReadingSerializer


class SLAConfigViewSet(viewsets.ModelViewSet):
    queryset = SLAConfig.objects.all()
    serializer_class = SLAConfigSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by('-started_at')
    serializer_class = AlertSerializer