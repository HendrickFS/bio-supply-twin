"""
Analytics utilities for the Digital Twin service.

Functions:
    - compute_compliance: Analyze telemetry data against SLA thresholds to determine compliance metrics.

"""

from typing import List, Dict, Any


def compute_compliance(telemetry_points: List[Dict[str, Any]], sla: Dict[str, float]) -> Dict[str, Any]:
    """
    Compute SLA compliance metrics for telemetry data points.
    
    Analyzes telemetry data against Service Level Agreement thresholds to determine
    the percentage of readings that fall within acceptable ranges and identify
    specific excursions (violations).
    
    Args:
        telemetry_points: List of telemetry readings
        sla: SLA configuration containing threshold values
    
    Returns:
        Dict containing:
            - num_points: Total number of telemetry points analyzed (int)
            - in_range_pct: Percentage of points within SLA thresholds (float, 0-100)
            - excursions: List of SLA violations
    """
    if not telemetry_points:
        return {
            "num_points": 0,
            "in_range_pct": 100.0,
            "excursions": [],
        }
    
    
    temp_min = sla["temp_min"]
    temp_max = sla["temp_max"]
    humidity_min = sla["humidity_min"]
    humidity_max = sla["humidity_max"]

    num_points = len(telemetry_points)
    points_in_range = 0
    excursions: List[Dict[str, Any]] = []

    for point in telemetry_points:
        temperature = point.get("temperature")
        humidity = point.get("humidity")
        
        temperature_ok = (temperature is None) or (temp_min <= temperature <= temp_max)
        humidity_ok = (humidity is None) or (humidity_min <= humidity <= humidity_max)
        
        if temperature_ok and humidity_ok:
            points_in_range += 1
        else:
            if temperature is not None and not temperature_ok:
                excursions.append({
                    "timestamp": point.get("timestamp"),
                    "metric": "temperature",
                    "value": temperature,
                    "band": [temp_min, temp_max],
                })
            if humidity is not None and not humidity_ok:
                excursions.append({
                    "timestamp": point.get("timestamp"),
                    "metric": "humidity",
                    "value": humidity,
                    "band": [humidity_min, humidity_max],
                })

    in_range_pct = (points_in_range / num_points) * 100.0
    
    return {
        "num_points": num_points,
        "in_range_pct": round(in_range_pct, 2),
        "excursions": excursions,
    }


