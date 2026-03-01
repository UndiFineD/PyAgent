# ObservabilityCore

**File**: `src\observability\stats\exporters\ObservabilityCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 68  
**Complexity**: 4 (simple)

## Overview

ObservabilityCore logic for metric aggregation and auditing.
Pure logic for summarizing agent performance and costs.

## Classes (2)

### `AgentMetric`

Class AgentMetric implementation.

### `ObservabilityCore`

Pure logic for processing agent telemetry data.

**Methods** (4):
- `__init__(self)`
- `process_metric(self, metric)`
- `summarize_performance(self)`
- `filter_by_time(self, start_iso, end_iso)`

## Dependencies

**Imports** (9):
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
