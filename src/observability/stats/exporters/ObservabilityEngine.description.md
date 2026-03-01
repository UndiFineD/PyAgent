# ObservabilityEngine

**File**: `src\observability\stats\exporters\ObservabilityEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 181  
**Complexity**: 10 (moderate)

## Overview

Engine for tracking agent performance, latency, and resource metrics.

## Classes (1)

### `ObservabilityEngine`

Provides telemetry and performance tracking for the agent fleet.

**Methods** (10):
- `__init__(self, workspace_root)`
- `log_event(self, agent_id, event_type, data, level)`
- `export_to_elk(self)`
- `get_metrics(self)`
- `start_trace(self, trace_id)`
- `end_trace(self, trace_id, agent_name, operation, status, input_tokens, output_tokens, model, metadata)`
- `trace_workflow(self, workflow_name, duration)`
- `get_summary(self)`
- `save(self)`
- `load(self)`

## Dependencies

**Imports** (15):
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.fleet.ResilientStubs.resilient_import`
- `src.classes.stats.ObservabilityCore.AgentMetric`
- `src.classes.stats.ObservabilityCore.ObservabilityCore`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
