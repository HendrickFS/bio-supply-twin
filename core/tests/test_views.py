"""
API/ViewSet tests for the core app.

Exercises list/create/retrieve endpoints with custom lookup fields.
"""

import pytest
from django.urls import reverse
from core.models import TransportBox, Sample

pytestmark = pytest.mark.django_db

def test_list_boxes(client, box):
    url = reverse("transportbox-list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert any(item["box_id"] == "BOX-001" for item in resp.data)

def test_create_box(client):
    url = reverse("transportbox-list")
    resp = client.post(
        url,
        {
            "box_id": "BOX-NEW",
            "geolocation": "40.7128,-74.0060",
            "temperature": 3.5,
            "humidity": 52.0,
            "status": "active",
        },
        content_type="application/json",
    )
    assert resp.status_code in (200, 201)
    assert TransportBox.objects.filter(box_id="BOX-NEW").exists()

def test_retrieve_box_by_box_id_lookup(client, box):
    url = reverse("transportbox-detail", kwargs={"box_id": "BOX-001"})
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.data["box_id"] == "BOX-001"

def test_sample_crud(client, box):
    list_url = reverse("sample-list")
    create = client.post(
        list_url,
        {
            "sample_id": "SMP-API",
            "box": box.id,
            "name": "Plasma",
            "description": "API created",
            "collected_at": "2024-01-01T00:00:00Z",
            "status": "collected",
            "temperature": 4.0,
            "humidity": 50.0,
        },
        content_type="application/json",
    )
    assert create.status_code in (200, 201)
    detail_url = reverse("sample-detail", kwargs={"sample_id": "SMP-API"})
    get_resp = client.get(detail_url)
    assert get_resp.status_code == 200
    assert get_resp.data["sample_id"] == "SMP-API"