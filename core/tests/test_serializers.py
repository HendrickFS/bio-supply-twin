"""
Serializer-layer tests for the core app.

Validates serialization output and input validation/saving behavior.
"""

import pytest
from django.utils import timezone
from core.serializers import TransportBoxSerializer, SampleSerializer

pytestmark = pytest.mark.django_db

def test_transport_box_serializer_round_trip(box):
    data = TransportBoxSerializer(box).data
    assert data["box_id"] == "BOX-001"
    assert "last_updated" in data

def test_sample_serializer_validation(box):
    payload = {
        "sample_id": "SMP-NEW",
        "box": box.id,
        "name": "Serum tube",
        "description": "Aliquot 1",
        "collected_at": timezone.now(),
        "status": "stored",
        "temperature": 5.0,
        "humidity": 50.0,
    }
    ser = SampleSerializer(data=payload)
    assert ser.is_valid(), ser.errors
    instance = ser.save()
    assert instance.box_id == box.id