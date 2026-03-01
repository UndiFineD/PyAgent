# MetricsEngine

**File**: `src\observability\stats\MetricsEngine.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 17 imports  
**Lines**: 280  
**Complexity**: 16 (moderate)

## Overview

Python module containing implementation for MetricsEngine.

## Classes (3)

### `ObservabilityEngine`

Provides telemetry and performance tracking for the agent fleet.

**Methods** (12):
- `__init__(self, workspace_root, fleet)`
- `log_event(self, agent_id, event_type, data, level)`
- `export_to_elk(self)`
- `get_metrics(self)`
- `generate_dashboard(self, shard_name)`
- `start_trace(self, trace_id)`
- `end_trace(self, trace_id, agent_name, operation, status, input_tokens, output_tokens, model, metadata)`
- `get_reliability_weights(self, agent_names)`
- `trace_workflow(self, workflow_name, duration)`
- `get_summary(self)`
- ... and 2 more methods

### `TokenCostEngine`

Class TokenCostEngine implementation.

**Methods** (2):
- `__init__(self)`
- `calculate_cost(self, model, input_tokens, output_tokens)`

### `ModelFallbackEngine`

Class ModelFallbackEngine implementation.

**Methods** (2):
- `__init__(self, cost_engine)`
- `get_fallback_model(self, current_model)`

## Dependencies

**Imports** (17):
- `MetricsCore.ModelFallbackCore`
- `MetricsCore.TokenCostCore`
- `ObservabilityCore.AgentMetric`
- `ObservabilityCore.ObservabilityCore`
- `__future__.annotations`
- `dataclasses.asdict`
- `exporters.MetricsExporter`
- `exporters.OTelManager`
- `exporters.PrometheusExporter`
- `json`
- `logging`
- `pathlib.Path`
- `psutil`
- `src.core.base.Version.VERSION`
- `src.observability.reports.GrafanaGenerator.GrafanaDashboardGenerator`
- ... and 2 more

---
*Auto-generated documentation*
