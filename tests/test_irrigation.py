from pathlib import Path

from yaku.irrigation import Reading, irrigation_plan, leak_alerts, load_readings


def r(m=40, up=10, down=10):
    return Reading("t", m, up, down)


def test_no_irrigation_when_moist():
    assert irrigation_plan([r(m=45)]) == []


def test_irrigation_duration_scales_with_deficit():
    assert irrigation_plan([r(m=25)], threshold=30, minutes_per_pct=4)[0][1] == 20


def test_irrigation_is_capped():
    assert irrigation_plan([r(m=0)], max_minutes=60)[0][1] == 60


def test_leak_detected_and_mentions_faina():
    alerts = leak_alerts([r(up=10, down=7)])
    assert len(alerts) == 1 and "faina" in alerts[0][2]


def test_no_leak_within_tolerance_and_zero_flow_safe():
    assert leak_alerts([r(up=10, down=9), r(up=0, down=0)]) == []


def test_sample_csv_loads():
    assert len(load_readings(Path(__file__).parent.parent / "data" / "sample_synthetic.csv")) == 6
