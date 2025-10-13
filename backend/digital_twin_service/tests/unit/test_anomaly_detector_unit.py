import pytest
from digital_twin_service.anomaly_detector import (
    AnomalyDetector, DetectionConfig, AnomalyAlgorithm
)

# Optional dependency: numpy. Skip tests if not installed.
np = pytest.importorskip("numpy")


@pytest.mark.parametrize("algorithm", [
    AnomalyAlgorithm.Z_SCORE,
    AnomalyAlgorithm.IQR,
    AnomalyAlgorithm.MOVING_AVERAGE,
])
def test_statistical_algorithms_detect_known_anomalies(algorithm):
    # Create synthetic data with clear anomalies
    normal = list(4.0 + 0.1 * np.random.randn(50))
    anomalies = [15.0, -5.0, 20.0]
    values = normal + anomalies + list(4.0 + 0.1 * np.random.randn(20))

    # Create telemetry points with timestamps
    telemetry = []
    from datetime import datetime, timedelta
    base = datetime.utcnow()
    for i, v in enumerate(values):
        telemetry.append({
            "timestamp": (base + timedelta(seconds=i)).isoformat(),
            "temperature": float(v),
            "humidity": 50.0
        })

    config = DetectionConfig(algorithm=algorithm, window_size=10)
    detector = AnomalyDetector(config)
    results = detector.detect_anomalies(telemetry, metrics=["temperature"])

    # Should detect at least the inserted anomalies
    assert any(r.value in anomalies for r in results), \
        "Algorithm failed to find inserted anomalies"


def test_convenience_functions_return_list():
    telemetry = [
        {"timestamp": "2025-01-01T00:00:00Z", "temperature": 5.0, 
         "humidity": 50.0}
    ] * 10
    detector = AnomalyDetector()
    results = detector.detect_anomalies(telemetry)
    assert isinstance(results, list)


def test_no_crash_on_empty_data():
    detector = AnomalyDetector()
    results = detector.detect_anomalies([])
    assert results == []
