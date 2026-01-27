"""
Real-Time Route Simulation Script
==================================

Purpose:
    Simulate a realistic journey for a transport box by sending telemetry data
    via MQTT that creates an actual route between locations over time.

Features:
    - Realistic route planning between cities
    - Gradual temperature and humidity changes
    - Time-based progression
    - Intermediate waypoints
    - Status updates based on journey phase
    - MQTT telemetry publishing

Usage:
    python simulate_route.py --box BOX-0001 --route "Boston->New York->Philadelphia"
    python simulate_route.py --box BOX-0001 --route "San Francisco->Los Angeles" --speed 5
    python simulate_route.py --box BOX-0001 --random --stops 5
    python simulate_route.py --box BOX-0001 --route "Boston->New York" --broker localhost --port 1883

"""

import paho.mqtt.client as mqtt
import json
import random
import time
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import math


MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# Major cities with GPS coordinates
CITIES = {
    "Boston": {"lat": 42.3601, "lng": -71.0589, "name": "Boston, MA"},
    "New York": {"lat": 40.7128, "lng": -74.0060, "name": "New York, NY"},
    "Philadelphia": {"lat": 39.9526, "lng": -75.1652, "name": "Philadelphia, PA"},
    "Washington DC": {"lat": 38.9072, "lng": -77.0369, "name": "Washington, DC"},
    "Chicago": {"lat": 41.8781, "lng": -87.6298, "name": "Chicago, IL"},
    "Detroit": {"lat": 42.3314, "lng": -83.0458, "name": "Detroit, MI"},
    "San Francisco": {"lat": 37.7749, "lng": -122.4194, "name": "San Francisco, CA"},
    "Los Angeles": {"lat": 34.0522, "lng": -118.2437, "name": "Los Angeles, CA"},
    "Seattle": {"lat": 47.6062, "lng": -122.3321, "name": "Seattle, WA"},
    "Portland": {"lat": 45.5152, "lng": -122.6784, "name": "Portland, OR"},
    "Miami": {"lat": 25.7617, "lng": -80.1918, "name": "Miami, FL"},
    "Atlanta": {"lat": 33.7490, "lng": -84.3880, "name": "Atlanta, GA"},
    "Dallas": {"lat": 32.7767, "lng": -96.7970, "name": "Dallas, TX"},
    "Houston": {"lat": 29.7604, "lng": -95.3698, "name": "Houston, TX"},
}

# Common routes
PREDEFINED_ROUTES = {
    "east_coast": ["Boston", "New York", "Philadelphia", "Washington DC"],
    "west_coast": ["Seattle", "Portland", "San Francisco", "Los Angeles"],
    "midwest": ["Chicago", "Detroit", "New York"],
    "south": ["Miami", "Atlanta", "Dallas", "Houston"],
    "cross_country": ["New York", "Chicago", "Denver", "San Francisco"],
}


class RouteSimulator:
    """Simulates a realistic journey with MQTT telemetry updates"""

    def __init__(self, broker: str = MQTT_BROKER, port: int = MQTT_PORT):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self._on_connect
        self.client.on_publish = self._on_publish
        self.connected = False
        
        # Connect to MQTT broker
        try:
            print(f"🔌 Connecting to MQTT broker at {broker}:{port}...")
            self.client.connect(broker, port, keepalive=60)
            self.client.loop_start()
            time.sleep(1)  # Wait for connection
            self.connected = True
            print("✅ Connected to MQTT broker")
        except Exception as e:
            print(f"❌ Failed to connect to MQTT broker: {e}")
            self.connected = False

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker"""
        if rc == 0:
            self.connected = True
        else:
            print(f"❌ Connection failed with code {rc}")
            self.connected = False

    def _on_publish(self, client, userdata, mid):
        """Callback for when a message is published"""
        pass

    def send_telemetry(self, box_id: str, lat: float, lng: float,
                      temperature: float, humidity: float, status: str = "in_transit",
                      timestamp: str = None) -> bool:
        """Send telemetry reading via MQTT"""
        if not self.connected:
            print("❌ Not connected to MQTT broker")
            return False

        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + "Z"

        telemetry_data = {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "geolocation": f"{lat},{lng}",
            "timestamp": timestamp,
            "status": status
        }

        try:
            topic = f"bio_supply/telemetry/box/{box_id}"
            payload = json.dumps(telemetry_data)
            result = self.client.publish(topic, payload, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                return True
            else:
                print(f"❌ Failed to publish telemetry: {result.rc}")
                return False
        except Exception as e:
            print(f"❌ Error sending telemetry: {e}")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            print("🔌 Disconnected from MQTT broker")

    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points in kilometers"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c

    def interpolate_route(self, start: Dict, end: Dict, num_points: int = 5) -> List[Tuple[float, float]]:
        """Generate intermediate waypoints between two locations"""
        waypoints = []
        
        for i in range(num_points + 1):
            ratio = i / num_points
            lat = start["lat"] + (end["lat"] - start["lat"]) * ratio
            lng = start["lng"] + (end["lng"] - start["lng"]) * ratio
            waypoints.append((lat, lng))
        
        return waypoints

    def simulate_environmental_changes(self, distance: float, base_temp: float = 5.0) -> Tuple[float, float]:
        """Simulate temperature and humidity changes based on distance traveled"""
        # Temperature variation based on distance and random factors
        temp_change = random.uniform(-0.5, 0.5) + (random.random() - 0.5) * 0.2
        temp = base_temp + temp_change
        temp = max(-5, min(15, temp))  # Clamp between -5 and 15°C
        
        # Humidity variation
        humidity = random.uniform(35, 65)
        
        return temp, humidity

    def simulate_route(self, box_id: str, cities: List[str], interval_seconds: int = 10,
                      waypoints_per_segment: int = 5):
        """Simulate a complete journey through multiple cities"""
        
        if len(cities) < 2:
            print("❌ Route must have at least 2 cities")
            return

        print("=" * 70)
        print(f"🚚 Starting Route Simulation for {box_id}")
        print(f"📍 Route: {' → '.join(cities)}")
        print(f"⏱️  Update interval: {interval_seconds}s")
        print(f"🗺️  Waypoints per segment: {waypoints_per_segment}")
        print("=" * 70)

        # Calculate total distance
        total_distance = 0
        for i in range(len(cities) - 1):
            start_city = CITIES[cities[i]]
            end_city = CITIES[cities[i + 1]]
            segment_distance = self.calculate_distance(
                start_city["lat"], start_city["lng"],
                end_city["lat"], end_city["lng"]
            )
            total_distance += segment_distance
            print(f"   {cities[i]} → {cities[i + 1]}: {segment_distance:.0f} km")

        print(f"\n📏 Total distance: {total_distance:.0f} km\n")

        # Initialize environmental conditions
        base_temp = random.uniform(3.0, 7.0)
        base_humidity = random.uniform(40.0, 60.0)
        
        waypoint_count = 0
        total_waypoints = len(cities) * waypoints_per_segment

        # Start journey
        for segment_idx in range(len(cities) - 1):
            start_city = CITIES[cities[segment_idx]]
            end_city = CITIES[cities[segment_idx + 1]]
            
            print(f"\n🛣️  Segment {segment_idx + 1}/{len(cities) - 1}: {cities[segment_idx]} → {cities[segment_idx + 1]}")
            
            # Generate waypoints for this segment
            waypoints = self.interpolate_route(start_city, end_city, waypoints_per_segment)
            
            for wp_idx, (lat, lng) in enumerate(waypoints):
                waypoint_count += 1
                
                # Determine status
                if waypoint_count == 1:
                    status = "active"
                    status_emoji = "🟢"
                elif waypoint_count == total_waypoints:
                    status = "delivered"
                    status_emoji = "🏁"
                elif wp_idx == 0:
                    status = "in_transit"
                    status_emoji = "🔵"
                else:
                    status = "in_transit"
                    status_emoji = "🔵"
                
                # Simulate environmental changes
                temp, humidity = self.simulate_environmental_changes(total_distance, base_temp)
                
                # Small gradual changes in base conditions
                base_temp += random.uniform(-0.3, 0.3)
                base_temp = max(2, min(8, base_temp))  # Keep in safe range mostly
                
                # Send telemetry
                location_name = f"{cities[segment_idx + 1] if wp_idx == waypoints_per_segment else cities[segment_idx]}"
                
                success = self.send_telemetry(box_id, lat, lng, temp, humidity, status)
                
                if success:
                    progress = (waypoint_count / total_waypoints) * 100
                    print(f"   {status_emoji} Waypoint {waypoint_count}/{total_waypoints} ({progress:.0f}%): "
                          f"{lat:.4f},{lng:.4f} | {temp:.1f}°C, {humidity:.0f}% | {status}")
                
                # Wait before next update (except for last waypoint)
                if waypoint_count < total_waypoints:
                    time.sleep(interval_seconds)

        print("\n" + "=" * 70)
        print(f"✅ Journey Complete! {box_id} has arrived at {cities[-1]}")
        print(f"📊 Total waypoints: {waypoint_count}") 
        print(f"⏱️  Total time: {(waypoint_count * interval_seconds) / 60:.1f} minutes")
        print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Simulate realistic route with telemetry data"
    )
    parser.add_argument(
        "--box",
        type=str,
        help="Box ID to simulate route for"
    )
    parser.add_argument(
        "--route",
        type=str,
        help="Route as 'City1->City2->City3' (use city names from predefined list)"
    )
    parser.add_argument(
        "--predefined",
        type=str,
        choices=list(PREDEFINED_ROUTES.keys()),
        help="Use a predefined route"
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Generate a random route"
    )
    parser.add_argument(
        "--stops",
        type=int,
        default=3,
        help="Number of stops for random route (default: 3)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Seconds between telemetry updates (default: 5)"
    )
    parser.add_argument(
        "--waypoints",
        type=int,
        default=4,
        help="Number of waypoints between each city (default: 4)"
    )
    parser.add_argument(
        "--broker",
        type=str,
        default=MQTT_BROKER,
        help=f"MQTT broker host (default: {MQTT_BROKER})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=MQTT_PORT,
        help=f"MQTT broker port (default: {MQTT_PORT})"
    )
    parser.add_argument(
        "--list-cities",
        action="store_true",
        help="List available cities and exit"
    )

    args = parser.parse_args()

    if args.list_cities:
        print("\n📍 Available Cities:\n")
        for city_name, info in sorted(CITIES.items()):
            print(f"   • {city_name:20} {info['name']}")
        print("\n🗺️  Predefined Routes:\n")
        for route_name, cities in PREDEFINED_ROUTES.items():
            print(f"   • {route_name:15} {' → '.join(cities)}")
        print()
        return

    if not args.box:
        print("❌ --box is required (unless using --list-cities)")
        return

    # Determine route
    if args.route:
        cities = [city.strip() for city in args.route.split("->")]
        # Validate cities
        for city in cities:
            if city not in CITIES:
                print(f"❌ Unknown city: {city}")
                print(f"💡 Use --list-cities to see available cities")
                return
    elif args.predefined:
        cities = PREDEFINED_ROUTES[args.predefined]
    elif args.random:
        cities = random.sample(list(CITIES.keys()), min(args.stops, len(CITIES)))
    else:
        print("❌ Please specify --route, --predefined, or --random")
        return

    simulator = RouteSimulator(args.broker, args.port)
    
    if not simulator.connected:
        print("❌ Failed to connect to MQTT broker. Exiting.")
        return
    
    try:
        simulator.simulate_route(args.box, cities, args.interval, args.waypoints)
    finally:
        simulator.disconnect()


if __name__ == "__main__":
    main()
