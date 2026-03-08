# TracingCore

**File**: `src\observability\stats\core\TracingCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 39  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for TracingCore.

## Classes (1)

### `TracingCore`

TracingCore handles the logic for distributed tracing and latency breakdown.
It prepares trace data for OpenTelemetry (OTel) exporters.

**Methods** (3):
- `create_span_context(self, trace_id, span_id)`
- `calculate_latency_breakdown(self, total_time, network_time)`
- `format_otel_log(self, name, attributes)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `time`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
