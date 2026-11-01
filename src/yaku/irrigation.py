"""Core logic for Yaku. Pure Python standard library: no network, no cloud, no uploads."""
import argparse
import csv
from dataclasses import dataclass


@dataclass
class Reading:
    timestamp: str
    soil_moisture_pct: float
    upstream_lps: float    # canal flow entering the segment, litres/second
    downstream_lps: float  # canal flow leaving the segment, litres/second


def load_readings(path):
    """Read a CSV with columns: timestamp, soil_moisture_pct, upstream_lps, downstream_lps."""
    with open(path, newline="", encoding="utf-8") as f:
        return [
            Reading(r["timestamp"], float(r["soil_moisture_pct"]),
                    float(r["upstream_lps"]), float(r["downstream_lps"]))
            for r in csv.DictReader(f)
        ]


def irrigation_plan(readings, threshold=30.0, minutes_per_pct=4.0, max_minutes=120.0):
    """Irrigate when soil moisture is below `threshold` (%).

    Duration grows with the deficit (minutes_per_pct per missing percentage point),
    capped at max_minutes so the soil is never flooded.
    """
    plan = []
    for r in readings:
        if r.soil_moisture_pct < threshold:
            deficit = threshold - r.soil_moisture_pct
            plan.append((r.timestamp, min(deficit * minutes_per_pct, max_minutes)))
    return plan


def leak_alerts(readings, tolerance=0.15):
    """Alert when downstream flow is more than `tolerance` (fraction) below upstream."""
    alerts = []
    for r in readings:
        if r.upstream_lps <= 0:
            continue
        loss = (r.upstream_lps - r.downstream_lps) / r.upstream_lps
        if loss > tolerance:
            alerts.append((r.timestamp, loss,
                           f"{r.timestamp}: {loss:.0%} of the water entering this canal segment "
                           f"does not arrive downstream. A leak is possible. "
                           f"Suggest the Assembly organise a faina to inspect and repair it."))
    return alerts


def main(argv=None):
    p = argparse.ArgumentParser(description="Yaku: irrigation timing and canal-leak alerts (offline).")
    p.add_argument("csv", help="path to readings CSV")
    p.add_argument("--threshold", type=float, default=30.0, help="soil moisture %% below which to irrigate")
    p.add_argument("--tolerance", type=float, default=0.15, help="allowed fractional flow loss")
    a = p.parse_args(argv)
    readings = load_readings(a.csv)
    print("== Irrigation plan ==")
    for ts, minutes in irrigation_plan(readings, a.threshold):
        print(f"{ts}: irrigate for {minutes:.0f} minutes")
    print("== Canal alerts ==")
    alerts = leak_alerts(readings, a.tolerance)
    for *_, msg in alerts:
        print(msg)
    if not alerts:
        print("No leaks detected.")


if __name__ == "__main__":
    main()
