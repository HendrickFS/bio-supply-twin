"""
Model-layer tests for the core app.

Covers string representations, relationships, and uniqueness constraints.
"""

import pytest
from django.db import IntegrityError
from core.models import TransportBox

pytestmark = pytest.mark.django_db

def test_transport_box_str(box):
    assert "BOX-001" in str(box)
    assert "Geolocation" in str(box)

def test_sample_fk_relationship(sample):
    assert sample.box.box_id == "BOX-001"
    assert sample in sample.box.samples.all()

def test_transport_box_box_id_unique_constraint():
    TransportBox.objects.create(
        box_id="UNIQ-1", geolocation="0,0", temperature=1.0, humidity=1.0, status="active"
    )
    with pytest.raises(IntegrityError):
        TransportBox.objects.create(
            box_id="UNIQ-1", geolocation="1,1", temperature=2.0, humidity=2.0, status="active"
        )