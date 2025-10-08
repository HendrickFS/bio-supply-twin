# core/management/commands/mqtt_consumer.py
import json
import logging
from contextlib import suppress

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_datetime

import paho.mqtt.client as mqtt

from core.models import TransportBox, Sample
from django.conf import settings

LOG = logging.getLogger("core.mqtt_consumer")


class Command(BaseCommand):
    help = "Run an MQTT consumer that persists bio_supply domain events into the DB."

    def add_arguments(self, parser):
        parser.add_argument("--broker", default="mqtt_broker",
                            help="MQTT broker host (default: mqtt_broker)")
        parser.add_argument("--port", type=int, default=1883,
                            help="MQTT broker port")

    def handle(self, *args, **options):
        broker = options["broker"]
        port = options["port"]

        client = mqtt.Client()
        client.on_connect = lambda c, u, f, rc: self._on_connect(c, u, f, rc)
        client.on_message = lambda c, u, m: self._on_message(c, u, m)

        LOG.info("Connecting to MQTT broker %s:%s", broker, port)
        client.connect(broker, port, keepalive=60)
        client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        LOG.info("Connected to MQTT (rc=%s). Subscribing to events...", rc)
        # Subscribe to domain events (adjust topics as your system uses them)
        client.subscribe("bio_supply/events/#")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception:
            LOG.exception("Invalid JSON on topic %s", msg.topic)
            return

        topic_parts = msg.topic.strip("/").split("/")
        # expected: bio_supply/events/<entity_type>/<entity_id>
        if len(topic_parts) < 4:
            LOG.warning("Unexpected topic format: %s", msg.topic)
            return

        _, _, entity_type, entity_id = topic_parts[:4]
        LOG.debug("Event received type=%s id=%s payload=%s", entity_type, entity_id, payload)

        if entity_type == "box":
            self._handle_box(entity_id, payload)
        elif entity_type == "sample":
            self._handle_sample(entity_id, payload)
        else:
            LOG.warning("Unknown entity_type %s on topic %s", entity_type, msg.topic)

    def _handle_box(self, box_id: str, payload: dict):
        # idempotent update
        defaults = {
            "geolocation": payload.get("geolocation", "unknown"),
            "temperature": payload.get("temperature", 0.0),
            "humidity": payload.get("humidity", 0.0),
            "status": payload.get("status", "unknown"),
        }
        try:
            with transaction.atomic():
                TransportBox.objects.update_or_create(box_id=box_id, defaults=defaults)
            LOG.info("Box %s upserted", box_id)
        except Exception:
            LOG.exception("Failed to upsert box %s", box_id)

    def _handle_sample(self, sample_id: str, payload: dict):
        # Ensure box exists (idempotent)
        try:
            with transaction.atomic():
                box_ref, _ = TransportBox.objects.get_or_create(
                    box_id=payload.get("box_id", "unknown"),
                    defaults={
                        "geolocation": payload.get("geolocation", "unknown"),
                        "temperature": payload.get("temperature", 0.0),
                        "humidity": payload.get("humidity", 0.0),
                        "status": "created_by_event",
                    },
                )

                collected_at = None
                if "collected_at" in payload:
                    with suppress(Exception):
                        collected_at = parse_datetime(payload["collected_at"])

                Sample.objects.update_or_create(
                    sample_id=sample_id,
                    defaults={
                        "box": box_ref,
                        "name": payload.get("name", ""),
                        "description": payload.get("description", ""),
                        "collected_at": collected_at,
                        "status": payload.get("status", "unknown"),
                        "temperature": payload.get("temperature", 0.0),
                        "humidity": payload.get("humidity", 0.0),
                    },
                )
            LOG.info("Sample %s upserted", sample_id)
        except Exception:
            LOG.exception("Failed to upsert sample %s", sample_id)