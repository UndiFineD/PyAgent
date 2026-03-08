# AgentMetrics

**File**: `src\classes\agent\AgentMetrics.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 130  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for AgentMetrics.

## Classes (1)

### `AgentMetrics`

Manages execution metrics and statistics for an agent.

**Methods** (7):
- `record_file_processed(self, modified)`
- `record_agent_applied(self, agent_name)`
- `finalize(self)`
- `get_summary(self, dry_run)`
- `to_dict(self)`
- `benchmark_execution(self, files, total_time_provided)`
- `cost_analysis(self, backend, cost_per_request)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
