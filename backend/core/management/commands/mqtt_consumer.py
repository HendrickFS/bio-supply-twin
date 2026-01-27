"""
Bio Supply Core Service - MQTT Consumer Command
==============================================

Purpose:
    Django management command that consumes MQTT messages from IoT sensors
    and updates biological sample and transport box records in real-time.
    Bridges IoT sensor data with Django ORM for persistent storage.

Key Features:
    - MQTT client with automatic reconnection
    - Real-time message processing and database updates
    - Topic-based routing for different data types
    - JSON payload parsing and validation
    - Django ORM integration for data persistence
    - Error handling and logging for reliability

MQTT Topics:
    - bio_supply/updates/sample/{SAMPLE_ID}: Sample sensor updates
    - bio_supply/updates/box/{BOX_ID}: Transport box sensor updates
    - bio_supply/telemetry/sample/{SAMPLE_ID}: Sample telemetry readings
    - bio_supply/telemetry/box/{BOX_ID}: Transport box telemetry readings

Message Format:
    JSON payload with sensor data (temperature, humidity, status, etc.)

Database Operations:
    - Creates or updates records
    - Creates telemetry readings and updates parent box/sample

Usage:
    python manage.py mqtt_consumer [--broker HOST] [--port PORT]

Dependencies:
    - paho-mqtt: MQTT client library
    - Django ORM: Database operations
    - core.models: Sample and TransportBox models

"""

import json
import logging
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
import paho.mqtt.client as mqtt
from core.models import TransportBox, Sample, TelemetryReading

LOG = logging.getLogger("core.mqtt_consumer")


class Command(BaseCommand):
    help = "Simple MQTT consumer that logs received messages."

    def add_arguments(self, parser):
        parser.add_argument("--broker", default="localhost",
                            help="MQTT broker host (default: localhost)")
        parser.add_argument("--port", type=int, default=1883,
                            help="MQTT broker port")

    def handle(self, *args, **options):
        broker = options["broker"]
        port = options["port"]

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.on_disconnect = self._on_disconnect

        print(f"Connecting to MQTT broker {broker}:{port}")
        print("Press Ctrl+C to stop.")
        
        try:
            client.connect(broker, port, keepalive=60)
            client.loop_forever()
        except KeyboardInterrupt:
            print("\nShutting down MQTT consumer...")
            client.disconnect()
        except Exception as e:
            print(f"Error: {e}")
            return

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected successfully (rc={rc})")
            client.subscribe("bio_supply/updates/#")
            client.subscribe("bio_supply/telemetry/#")
            print("Listening for messages on bio_supply/updates/# and bio_supply/telemetry/#")
        else:
            print(f"Connection failed (rc={rc})")

    def _on_disconnect(self, client, userdata, rc):
        print(f"Disconnected (rc={rc})")

    def _on_message(self, client, userdata, msg):
        print(f"Message received - Topic: {msg.topic}")
        
        # Extract topic type, model type and ID
        # bio_supply/updates/sample/SAMPLE-0001 or bio_supply/telemetry/box/BOX-0001
        topic_parts = msg.topic.split("/")
        if len(topic_parts) >= 4:
            topic_type = topic_parts[1]  # "updates" or "telemetry"
            model_type = topic_parts[2]  # "sample" or "box"
            model_id = topic_parts[3]    # "SAMPLE-0001" or "BOX-0001"
            
            try:
                payload = json.loads(msg.payload.decode('utf-8'))
                print(f"Processing {topic_type}/{model_type}: {model_id}")
                
                if topic_type == "updates":
                    if model_type == "sample":
                        self._update_sample(model_id, payload)
                    elif model_type == "box":
                        self._update_box(model_id, payload)
                    else:
                        print(f"Unknown model type: {model_type}")
                        
                elif topic_type == "telemetry":
                    if model_type == "sample":
                        self._process_sample_telemetry(model_id, payload)
                    elif model_type == "box":
                        self._process_box_telemetry(model_id, payload)
                    else:
                        print(f"Unknown model type: {model_type}")
                else:
                    print(f"Unknown topic type: {topic_type}")
                    
            except json.JSONDecodeError as e:
                print(f"Invalid JSON payload: {e}")
        else:
            print(f"Invalid topic format: {msg.topic}")
        
        print("-" * 30)

    def _update_sample(self, sample_id, payload):
        try:
            # Get or create default transport box
            default_box, _ = TransportBox.objects.get_or_create(
                box_id="DEFAULT-BOX",
                defaults={
                    'geolocation': 'unknown',
                    'temperature': 0.0,
                    'humidity': 0.0,
                    'status': 'default',
                }
            )
            
            # Get or create the sample
            sample, created = Sample.objects.get_or_create(
                sample_id=sample_id,
                defaults={
                    'name': payload.get('name', ''),
                    'description': payload.get('description', ''),
                    'status': payload.get('status', 'unknown'),
                    'temperature': payload.get('temperature', 0.0),
                    'humidity': payload.get('humidity', 0.0),
                    'collected_at': parse_datetime(payload.get('collected_at')) if payload.get('collected_at') else None,
                    'box': default_box
                }
            )
            
            if not created:
                # Update existing sample
                for field, value in payload.items():
                    if hasattr(sample, field):
                        if field == 'collected_at' and value:
                            setattr(sample, field, parse_datetime(value))
                        else:
                            setattr(sample, field, value)
                sample.save()
            
            print(f"{'Created' if created else 'Updated'} sample: {sample_id}")
            
        except Exception as e:
            print(f"Error updating sample {sample_id}: {e}")

    def _update_box(self, box_id, payload):
        try:
            box, created = TransportBox.objects.get_or_create(
                box_id=box_id,
                defaults={
                    'geolocation': payload.get('geolocation', 'unknown'),
                    'temperature': payload.get('temperature', 0.0),
                    'humidity': payload.get('humidity', 0.0),
                    'status': payload.get('status', 'unknown'),
                }
            )
            
            if not created:
                # Update existing box
                for field, value in payload.items():
                    if hasattr(box, field):
                        setattr(box, field, value)
                box.save()
            
            print(f"{'Created' if created else 'Updated'} box: {box_id}")
            
        except Exception as e:
            print(f"Error updating box {box_id}: {e}")

    def _process_box_telemetry(self, box_id, payload):
        """Process telemetry reading for a transport box and update the box"""
        try:
            # Get or create the box
            box, created = TransportBox.objects.get_or_create(
                box_id=box_id,
                defaults={
                    'geolocation': payload.get('geolocation', 'unknown'),
                    'temperature': payload.get('temperature', 0.0),
                    'humidity': payload.get('humidity', 0.0),
                    'status': 'active',
                }
            )
            
            # Create telemetry reading
            telemetry = TelemetryReading.objects.create(
                box=box,
                sample=None,
                timestamp=parse_datetime(payload.get('timestamp')) if payload.get('timestamp') else None,
                temperature=payload.get('temperature', 0.0),
                humidity=payload.get('humidity', 0.0),
                geolocation=payload.get('geolocation', box.geolocation)
            )
            
            # Update box with latest telemetry data
            box.temperature = payload.get('temperature', box.temperature)
            box.humidity = payload.get('humidity', box.humidity)
            if payload.get('geolocation'):
                box.geolocation = payload.get('geolocation')
            if payload.get('status'):
                box.status = payload.get('status')
            box.save()
            
            print(f"Created telemetry reading for box {box_id} and updated box")
            
        except Exception as e:
            print(f"Error processing telemetry for box {box_id}: {e}")

    def _process_sample_telemetry(self, sample_id, payload):
        """Process telemetry reading for a sample and update the sample"""
        try:
            # Get the sample (must exist)
            sample = Sample.objects.get(sample_id=sample_id)
            
            # Create telemetry reading
            telemetry = TelemetryReading.objects.create(
                box=sample.box,
                sample=sample,
                timestamp=parse_datetime(payload.get('timestamp')) if payload.get('timestamp') else None,
                temperature=payload.get('temperature', 0.0),
                humidity=payload.get('humidity', 0.0),
                geolocation=payload.get('geolocation', sample.box.geolocation if sample.box else 'unknown')
            )
            
            # Update sample with latest telemetry data
            sample.temperature = payload.get('temperature', sample.temperature)
            sample.humidity = payload.get('humidity', sample.humidity)
            if payload.get('status'):
                sample.status = payload.get('status')
            sample.save()
            
            print(f"Created telemetry reading for sample {sample_id} and updated sample")
            
        except Sample.DoesNotExist:
            print(f"Sample {sample_id} does not exist. Create it first via updates topic.")
        except Exception as e:
            print(f"Error processing telemetry for sample {sample_id}: {e}")