# simple_test.py - Test MQTT updates
import paho.mqtt.client as mqtt
import json
import time

def send_updates():
    print("🚀 Sending MQTT updates to server...")
    
    # Connect to MQTT broker
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    
    # Test messages
    messages = [
        {
            "topic": "bio_supply/updates/sample/MQTT-TEST-001",
            "data": {
                "name": "Test Sample from MQTT",
                "temperature": 1000,
                "humidity": 70.2,
                "status": "received",
                "collected_at": "2024-10-08T23:45:00Z"
            }
        },
        {
            "topic": "bio_supply/updates/box/MQTT-BOX-001", 
            "data": {
                "geolocation": "40.7128,-74.0060",
                "temperature": 22.1,
                "humidity": 58.3,
                "status": "in_transit"
            }
        },
        {
            "topic": "bio_supply/updates/sample/MY-SAMPLE-ID",
            "data": {
                "name": "My Sample", 
                "temperature": 4.9, 
                "status": "active"
            }
        }
    ]
    
    # Send all messages
    for msg in messages:
        message_json = json.dumps(msg["data"])
        client.publish(msg["topic"], message_json)
        print(f"✅ Sent to {msg['topic']}")
        print(f"📄 Data: {msg['data']}")
        print()
        time.sleep(0.5)  # Small delay between messages
    
    client.disconnect()
    print("🔌 Disconnected from MQTT broker")

if __name__ == "__main__":
    send_updates()