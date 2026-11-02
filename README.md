# Yaku 💧

*Yaku* is Quechua for "water". Yaku is a small, **offline** tool that reads soil-moisture and canal-flow readings from a CSV and tells a community:

1. **When and for how long to irrigate** (simple soil water balance), and
2. **A plain-language alert if a canal segment is losing water** (upstream flow minus downstream flow beyond a tolerance), written so a Community Assembly can use it to organise a *faina* (collective work day).

## Why

Water-development projects often arrive as heavy drilling, concrete channels and foreign-owned machinery that disrupt sacred landscapes, create maintenance dependence and impose debt. Yaku starts from a different premise: communities already have working systems of water governance, such as canals (*kanalas*), collective labour (*faina*, *ayni*) and intergenerational hydrological knowledge. Technology should adapt to those systems, not the other way around. Yaku is a non-invasive, open-source tool to analyse and protect what a community already has, and its data stays under the community's control. It runs on a laptop and needs no cloud. See [DATA_SOVEREIGNTY.md](DATA_SOVEREIGNTY.md).

This is a small proof of concept. It is **not** a validated hydrological model and should be calibrated with the community that uses it.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
yaku data/sample_synthetic.csv
pytest
```

CSV columns: `timestamp, soil_moisture_pct, upstream_lps, downstream_lps`.
The sample file is **synthetic (fake)** and represents no real community.

## Example output

```
== Irrigation plan ==
2026-01-03 06:00: irrigate for 8 minutes
2026-01-04 06:00: irrigate for 22 minutes
2026-01-05 06:00: irrigate for 36 minutes
== Canal alerts ==
2026-01-04 06:00: 21% of the water entering this canal segment does not arrive downstream. A leak is possible. Suggest the Assembly organise a faina to inspect and repair it.
2026-01-05 06:00: 28% of the water entering this canal segment does not arrive downstream. A leak is possible. Suggest the Assembly organise a faina to inspect and repair it.
```

Options: `--threshold 30` (moisture % below which to irrigate), `--tolerance 0.15` (allowed fractional flow loss).

## Who can help (cross-disciplinary)

Hydrologists, agronomists, anthropologists, data-governance and policy students, translators (Spanish, Quechua, and other Indigenous languages), and Python beginners all have a role. Domain knowledge from the communities that would use a tool like this comes first; code comes second.

## Limitations

Proof of concept with simple, transparent rules (no machine learning yet). Not validated against real canals. Thresholds must be set with the people who know the land.

## Contributing

Welcome, especially translations and community-led improvements. See [CONTRIBUTING.md](CONTRIBUTING.md) and the issues labelled `good first issue`. Licensed under [Apache 2.0](LICENSE).
