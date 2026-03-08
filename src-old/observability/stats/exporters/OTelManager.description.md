# OTelManager

**File**: `src\observability\stats\exporters\OTelManager.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 13 imports  
**Lines**: 161  
**Complexity**: 5 (moderate)

## Overview

Distributed tracing for the PyAgent fleet using OpenTelemetry standards.
Allows visualization of agent chains and request propagation across nodes.

## Classes (2)

### `Span`

Class Span implementation.

### `OTelManager`

Manages OTel-compatible spans and traces for cross-fleet observability.
Integrated with TracingCore for latency analysis and OTel formatting.

**Methods** (5):
- `__init__(self)`
- `start_span(self, name, parent_id, attributes)`
- `end_span(self, span_id, status, network_latency_sec, attributes)`
- `export_spans(self)`
- `get_trace_context(self, span_id)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `opentelemetry.sdk.resources.Resource`
- `opentelemetry.sdk.trace.TracerProvider`
- `opentelemetry.trace`
- `src.core.base.Version.VERSION`
- `src.observability.stats.core.TracingCore.TracingCore`
- `threading`
- `time`
- `typing.Any`
- `uuid`

---
*Auto-generated documentation*
