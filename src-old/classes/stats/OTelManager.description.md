# OTelManager

**File**: `src\classes\stats\OTelManager.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 10 imports  
**Lines**: 86  
**Complexity**: 5 (moderate)

## Overview

Distributed tracing for the PyAgent fleet using OpenTelemetry standards.
Allows visualization of agent chains and request propagation across nodes.

## Classes (2)

### `Span`

Class Span implementation.

### `OTelManager`

Manages OTel-compatible spans and traces for cross-fleet observability.

**Methods** (5):
- `__init__(self)`
- `start_span(self, name, parent_id, attributes)`
- `end_span(self, span_id, status, attributes)`
- `export_spans(self)`
- `get_trace_context(self, span_id)`

## Dependencies

**Imports** (10):
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
