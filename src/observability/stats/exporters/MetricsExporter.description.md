# MetricsExporter

**File**: `src\observability\stats\exporters\MetricsExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 61  
**Complexity**: 5 (moderate)

## Overview

Exporter for high-level fleet metrics.
Sends telemetry to specialized backends like Prometheus, InfluxDB, or Grafana Cloud.

## Classes (1)

### `MetricsExporter`

Consolidates all fleet telemetry and exposes it for external monitoring.

**Methods** (5):
- `__init__(self)`
- `record_agent_call(self, agent_name, duration_ms, success)`
- `record_resource_usage(self, cpu_percent, mem_mb)`
- `get_prometheus_payload(self)`
- `export_to_grafana(self)`

## Dependencies

**Imports** (5):
- `PrometheusExporter.PrometheusExporter`
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `time`

---
*Auto-generated documentation*
