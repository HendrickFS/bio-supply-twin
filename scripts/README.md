# Bio Supply Twin - Scripts

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Route Simulation (MQTT)

The `simulate_route.py` script simulates realistic transport box journeys by sending telemetry data via MQTT.

### Prerequisites

- MQTT broker running (default: localhost:1883)
- Django MQTT consumer running: `python manage.py mqtt_consumer`

### Basic Usage

```bash
# Simulate Boston → New York → Philadelphia route
python simulate_route.py --box BOX-0001 --route "Boston->New York->Philadelphia"

# Use predefined route with custom interval
python simulate_route.py --box BOX-0002 --predefined west_coast --interval 3

# Random route with 5 stops
python simulate_route.py --box BOX-0003 --random --stops 5

# Custom MQTT broker
python simulate_route.py --box BOX-0001 --route "Boston->New York" --broker mqtt.example.com --port 1883
```

### Options

- `--box BOX_ID`: Transport box identifier (required)
- `--route "City1->City2->City3"`: Custom route between cities
- `--predefined ROUTE`: Use predefined route (east_coast, west_coast, midwest, south, cross_country)
- `--random`: Generate random route
- `--stops N`: Number of stops for random route (default: 3)
- `--interval N`: Seconds between updates (default: 5)
- `--waypoints N`: Waypoints between cities (default: 4)
- `--broker HOST`: MQTT broker host (default: localhost)
- `--port PORT`: MQTT broker port (default: 1883)
- `--list-cities`: Show available cities and routes


## Available Cities

- Boston, New York, Philadelphia, Washington DC
- Chicago, Detroit
- San Francisco, Los Angeles, Seattle, Portland
- Miami, Atlanta, Dallas, Houston

## Predefined Routes

- **east_coast**: Boston → New York → Philadelphia → Washington DC
- **west_coast**: Seattle → Portland → San Francisco → Los Angeles
- **midwest**: Chicago → Detroit → New York
- **south**: Miami → Atlanta → Dallas → Houston
- **cross_country**: New York → Chicago → Denver → San Francisco
