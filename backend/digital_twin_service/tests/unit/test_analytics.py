import pytest
from digital_twin_service.analytics import compute_compliance


@pytest.fixture
def sla():
    return {"temp_min": 2.0, "temp_max": 8.0, "humidity_min": 30.0, "humidity_max": 60.0}


def test_empty_telemetry_returns_100_percent(sla):
    res = compute_compliance([], sla)
    assert res["num_points"] == 0
    assert res["in_range_pct"] == 100.0
    assert res["excursions"] == []


def test_all_in_range(sla):
    telemetry = [
        {"timestamp": "t1", "temperature": 4.0, "humidity": 45.0},
        {"timestamp": "t2", "temperature": 3.0, "humidity": 50.0},
    ]
    res = compute_compliance(telemetry, sla)
    assert res["num_points"] == 2
    assert res["in_range_pct"] == 100.0
    assert res["excursions"] == []


def test_temperature_excursions(sla):
    telemetry = [
        {"timestamp": "t1", "temperature": 10.0, "humidity": 50.0},
        {"timestamp": "t2", "temperature": 4.0, "humidity": 50.0},
    ]
    res = compute_compliance(telemetry, sla)
    assert res["num_points"] == 2
    assert res["in_range_pct"] == 50.0
    assert len(res["excursions"]) == 1
    ex = res["excursions"][0]
    assert ex["metric"] == "temperature"
    assert ex["value"] == 10.0


def test_humidity_excursions(sla):
    telemetry = [
        {"timestamp": "t1", "temperature": 4.0, "humidity": 70.0},
        {"timestamp": "t2", "temperature": 4.0, "humidity": 50.0},
    ]
    res = compute_compliance(telemetry, sla)
    assert res["in_range_pct"] == 50.0
    assert len(res["excursions"]) == 1
    assert res["excursions"][0]["metric"] == "humidity"


def test_mixed_excursions(sla):
    telemetry = [
        {"timestamp": "t1", "temperature": 10.0, "humidity": 70.0},
        {"timestamp": "t2", "temperature": 4.0, "humidity": 50.0},
    ]
    res = compute_compliance(telemetry, sla)
    assert res["in_range_pct"] == 50.0
    assert len(res["excursions"]) == 2
    metrics = {e["metric"] for e in res["excursions"]}
    assert metrics == {"temperature", "humidity"}


def test_missing_values_count_as_ok(sla):
    telemetry = [
        {"timestamp": "t1", "temperature": None, "humidity": 50.0},
        {"timestamp": "t2", "temperature": 4.0, "humidity": None},
        {"timestamp": "t3", "temperature": None, "humidity": None},
    ]
    res = compute_compliance(telemetry, sla)
    assert res["num_points"] == 3
    assert res["in_range_pct"] == 100.0
    assert res["excursions"] == []


def test_rounding_of_percentage(sla):
    telemetry = [
        {"timestamp": "t1", "temperature": 4.0, "humidity": 50.0},
        {"timestamp": "t2", "temperature": 10.0, "humidity": 50.0},
        {"timestamp": "t3", "temperature": 4.0, "humidity": 50.0},
    ]
    res = compute_compliance(telemetry, sla)
    assert res["num_points"] == 3
    # 2 in range out of 3 => 66.666... rounded to 66.67
    assert res["in_range_pct"] == 66.67
