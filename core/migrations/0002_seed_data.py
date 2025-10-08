"""Data migration to seed initial TransportBox and Sample rows.

This migration is idempotent and uses apps.get_model to work with
historical models during migrations. It also supplies a reverse function
to remove the seeded rows if the migration is unapplied.
"""

from django.db import migrations
import datetime


def seed_data(apps, schema_editor):
    TransportBox = apps.get_model('core', 'TransportBox')
    Sample = apps.get_model('core', 'Sample')

    boxes = [
        {
            'box_id': 'BOX-0001',
            'geolocation': '52.5200,13.4050',
            'temperature': 4.0,
            'humidity': 50.0,
            'status': 'in_transit',
        },
        {
            'box_id': 'BOX-0002',
            'geolocation': '51.5074,-0.1278',
            'temperature': 2.5,
            'humidity': 48.0,
            'status': 'idle',
        },
    ]

    for b in boxes:
        TransportBox.objects.update_or_create(
            box_id=b['box_id'],
            defaults={
                'geolocation': b['geolocation'],
                'temperature': b['temperature'],
                'humidity': b['humidity'],
                'status': b['status'],
            }
        )

    samples = [
        {
            'sample_id': 'SAMPLE-0001',
            'box_id': 'BOX-0001',
            'name': 'Blood Sample A',
            'description': 'Control sample A',
            'collected_at': datetime.datetime(2025, 1, 1, 10, 0, 0),
            'status': 'collected',
            'temperature': 4.0,
            'humidity': 50.0,
        },
        {
            'sample_id': 'SAMPLE-0002',
            'box_id': 'BOX-0002',
            'name': 'Vaccine Batch 1',
            'description': 'Test vaccine batch',
            'collected_at': datetime.datetime(2025, 1, 2, 11, 30, 0),
            'status': 'stored',
            'temperature': 2.5,
            'humidity': 48.0,
        },
    ]

    for s in samples:
        box_ref, _ = TransportBox.objects.get_or_create(
            box_id=s['box_id'],
            defaults={
                'geolocation': 'unknown',
                'temperature': s['temperature'],
                'humidity': s['humidity'],
                'status': 'created_by_migration',
            }
        )
        Sample.objects.update_or_create(
            sample_id=s['sample_id'],
            defaults={
                'box': box_ref,
                'name': s['name'],
                'description': s['description'],
                'collected_at': s['collected_at'],
                'status': s['status'],
                'temperature': s['temperature'],
                'humidity': s['humidity'],
            }
        )


def unseed_data(apps, schema_editor):
    TransportBox = apps.get_model('core', 'TransportBox')
    Sample = apps.get_model('core', 'Sample')

    Sample.objects.filter(sample_id__in=['SAMPLE-0001', 'SAMPLE-0002']).delete()
    TransportBox.objects.filter(box_id__in=['BOX-0001', 'BOX-0002']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]