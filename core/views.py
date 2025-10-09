"""
Bio Supply Core Service - Django REST API Views
==============================================

Purpose:
    Django REST Framework ViewSets for biological supply chain API endpoints.
    Provides CRUD operations for transport boxes and biological samples
    with RESTful API interface for external systems and frontend applications.

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
from .models import TransportBox, Sample
from .serializers import TransportBoxSerializer, SampleSerializer


class TransportBoxViewSet(viewsets.ModelViewSet):
    queryset = TransportBox.objects.all()
    serializer_class = TransportBoxSerializer
    lookup_field = 'box_id'

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    lookup_field = 'sample_id'