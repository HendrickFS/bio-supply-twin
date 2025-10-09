# core/management/commands/mqtt_consumer.py
import json
import logging
import os
import django
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
import paho.mqtt.client as mqtt
from core.models import TransportBox, Sample

# Ensure Django is configured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bio_supply_twin.settings')
django.setup()

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
        client.on_subscribe = self._on_subscribe

        print(f"🔄 Connecting to MQTT broker {broker}:{port}")
        print("Consumer will run continuously. Press Ctrl+C to stop.")
        
        try:
            print("🔄 Attempting connection...")
            result = client.connect(broker, port, keepalive=60)
            print(f"🔍 Connection attempt result: {result}")
            print("🔄 Starting event loop...")
            client.loop_forever()
        except KeyboardInterrupt:
            print("\nShutting down MQTT consumer...")
            client.disconnect()
        except Exception as e:
            print(f"Error: {e}")
            print("Consumer stopped unexpectedly")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"✅ Connected to MQTT successfully (rc={rc})")
            result = client.subscribe("bio_supply/updates/#")
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                print("✅ Successfully subscribed to bio_supply/updates/#")
            else:
                print(f"❌ Failed to subscribe (error code: {result[0]})")
            print("🔊 Listening for messages...")
        else:
            print(f"❌ Failed to connect to MQTT (rc={rc})")
            if rc == 1:
                print("   Connection refused - incorrect protocol version")
            elif rc == 2:
                print("   Connection refused - invalid client identifier")
            elif rc == 3:
                print("   Connection refused - server unavailable")
            elif rc == 4:
                print("   Connection refused - bad username or password")
            elif rc == 5:
                print("   Connection refused - not authorised")

    def _on_disconnect(self, client, userdata, rc):
        print(f"Disconnected from MQTT (rc={rc})")

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"✅ Subscription confirmed (mid={mid}, qos={granted_qos})")
        print("🔍 Now publishing test message to verify connection...")
        # Send a test message to verify the loop is working
        client.publish("bio_supply/updates/test", "connection_test")

    def _on_message(self, client, userdata, msg):
        print(f"📨 MESSAGE RECEIVED!")
        print(f"Topic: {msg.topic}")
        print(f"Payload: {msg.payload.decode('utf-8')}")
        
        # Extract model type and ID from topic like: bio_supply/updates/sample/SAMPLE-0001
        topic_parts = msg.topic.split("/")
        if len(topic_parts) >= 4:
            model_type = topic_parts[2]  # e.g., "sample"
            model_id = topic_parts[3]    # e.g., "SAMPLE-0001"
            print(f"Processing {model_type.title()} Update: {model_id}")
            
            # Parse the message payload
            try:
                payload = json.loads(msg.payload.decode('utf-8'))
                print(f"Parsed payload: {payload}")
                
                # Update the correct model
                if model_type == "sample":
                    self._update_sample(model_id, payload)
                elif model_type == "box":
                    self._update_box(model_id, payload)
                else:
                    print(f"❌ Unknown model type: {model_type}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON payload: {e}")
                print(f"Raw payload: {msg.payload.decode('utf-8')}")
        else:
            print(f"❌ Unexpected topic format: {msg.topic}")
        
        print("-" * 50)

    def _update_sample(self, sample_id, payload):
        try:
            # Get or create a default transport box if needed
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
                    'box': default_box  # Use the box object, not box_id
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
            
            action = "Created" if created else "Updated"
            print(f"{action} sample: {sample_id}")
            
        except Exception as e:
            print(f"Error updating sample {sample_id}: {e}")

    def _update_box(self, box_id, payload):
        try:
            # Get or create the box
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
            
            action = "Created" if created else "Updated"
            print(f"{action} box: {box_id}")
            
        except Exception as e:
            print(f"Error updating box {box_id}: {e}")