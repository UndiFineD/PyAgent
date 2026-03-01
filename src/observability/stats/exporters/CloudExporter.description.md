# CloudExporter

**File**: `src\observability\stats\exporters\CloudExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 165  
**Complexity**: 8 (moderate)

## Overview

Auto-extracted class from agent_stats.py

## Classes (1)

### `CloudExporter`

Export stats to cloud monitoring services.

Supports exporting metrics to Datadog, Prometheus, Grafana,
and other cloud monitoring platforms.

Attributes:
    destination: The export destination.
    config: Export configuration.
    export_queue: Queued metrics for export.

**Methods** (8):
- `__init__(self, destination, api_key, endpoint)`
- `_get_default_endpoint(self)`
- `queue_metric(self, metric)`
- `export(self)`
- `_export_datadog(self)`
- `_export_prometheus(self)`
- `_export_generic(self)`
- `get_export_stats(self)`

## Dependencies

**Imports** (9):
- `ObservabilityCore.ExportDestination`
- `ObservabilityCore.Metric`
- `__future__.annotations`
- `datetime.datetime`
- `json`
- `logging`
- `os`
- `src.core.base.Version.VERSION`
- `typing.Any`

---
*Auto-generated documentation*
