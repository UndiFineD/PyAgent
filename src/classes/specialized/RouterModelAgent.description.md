# RouterModelAgent

**File**: `src\classes\specialized\RouterModelAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 93  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for RouterModelAgent.

## Classes (1)

### `RouterModelAgent`

**Inherits from**: BaseAgent

Intelligently routes tasks to different LLMs based on cost, latency, 
and task complexity.

**Methods** (4):
- `__init__(self, path)`
- `determine_optimal_provider(self, task_type, max_cost, required_capability)`
- `compress_context(self, long_prompt, target_tokens)`
- `get_routing_stats(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
