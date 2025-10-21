import requests

# Check boxes
print("Checking boxes in database...")
try:
    response = requests.get("http://localhost:8001/api/transport_boxes/")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        boxes = response.json()
        print(f"\n✅ Found {len(boxes)} boxes:")
        for box in boxes:
            print(f"  - {box['box_id']} | {box['geolocation']} | {box['status']}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# Try to get specific box
print("\n" + "="*50)
box_id = "BOX-0001"
print(f"Trying to fetch {box_id}...")
try:
    response = requests.get(f"http://localhost:8001/api/transport_boxes/{box_id}/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Box found: {response.json()}")
    else:
        print(f"❌ Box not found")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
