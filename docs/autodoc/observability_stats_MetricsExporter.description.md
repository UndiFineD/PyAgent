# Description: `MetricsExporter.py`

## Module purpose

Exporter for high-level fleet metrics.
Sends telemetry to specialized backends like Prometheus, InfluxDB, or Grafana Cloud.

## Location
- Path: `observability\stats\MetricsExporter.py`

## Public surface
- Classes: MetricsExporter
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `__future__`, `logging`, `time`, `typing`, `src.observability.stats.PrometheusExporter`

## Metadata

- SHA256(source): `9ea369c207cad73c`
- Last updated: `2026-01-11 12:55:46`
- File: `observability\stats\MetricsExporter.py`