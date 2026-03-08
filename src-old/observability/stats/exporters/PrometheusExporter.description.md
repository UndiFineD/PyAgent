# PrometheusExporter

**File**: `src\observability\stats\exporters\PrometheusExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 59  
**Complexity**: 4 (simple)

## Overview

Exporter for fleet metrics in Prometheus/OpenMetrics format.
Enables real-time dashboards in Grafana and ELK stack.

## Classes (1)

### `PrometheusExporter`

Formats fleet telemetry into Prometheus-compatible metrics.

**Methods** (4):
- `__init__(self)`
- `record_metric(self, name, value, labels)`
- `generate_scrape_response(self)`
- `get_grafana_info(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
