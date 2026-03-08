# AgentMetrics

**File**: `src\core\base\common\utils\AgentMetrics.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 113  
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

**Imports** (7):
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
