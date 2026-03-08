# RLSelector

**File**: `src\classes\orchestration\RLSelector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 61  
**Complexity**: 4 (simple)

## Overview

Reinforcement Learning based tool selector.
Optimizes tool selection by weighting success rates and historical performance.

## Classes (1)

### `RLSelector`

Uses a Multi-Armed Bandit strategy to optimize tool selection.

**Methods** (4):
- `__init__(self)`
- `update_stats(self, tool_name, success)`
- `select_best_tool(self, candidate_tools)`
- `get_policy_summary(self)`

## Dependencies

**Imports** (6):
- `logging`
- `random`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
