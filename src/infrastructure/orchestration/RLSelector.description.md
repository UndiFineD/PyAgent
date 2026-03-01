# RLSelector

**File**: `src\infrastructure\orchestration\RLSelector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 95  
**Complexity**: 4 (simple)

## Overview

Reinforcement Learning based tool selector.
Optimizes tool selection by weighting success rates and historical performance.

## Classes (1)

### `RLSelector`

Uses Bayesian Thompson Sampling to optimize tool selection under uncertainty.

**Methods** (4):
- `__init__(self)`
- `update_stats(self, tool_name, success)`
- `select_best_tool(self, candidate_tools)`
- `get_policy_summary(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `random`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
