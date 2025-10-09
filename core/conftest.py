"""
Test fixtures for the core app.

Provides reusable ORM-backed fixtures for TransportBox and Sample.
"""

import pytest
from django.utils import timezone
from core.models import TransportBox, Sample

@pytest.fixture
def box():
    return TransportBox.objects.create(
        box_id="BOX-001",
        geolocation="51.5074,-0.1278",
        temperature=4.2,
        humidity=55.0,
        status="active",
    )

@pytest.fixture
def sample(box):
    return Sample.objects.create(
        sample_id="SMP-001",
        box=box,
        name="Blood vial A",
        description="Primary sample",
        collected_at=timezone.now(),
        status="collected",
        temperature=4.1,
        humidity=54.0,
    )