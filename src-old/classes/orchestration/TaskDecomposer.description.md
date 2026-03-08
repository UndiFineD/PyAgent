# TaskDecomposer

**File**: `src\classes\orchestration\TaskDecomposer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 31  
**Complexity**: 3 (simple)

## Overview

Engine for dynamic task decomposition.
Breaks complex user requests into granular sub-tasks for the agent fleet.

## Classes (1)

### `TaskDecomposer`

Analyzes high-level requests and generates a multi-step plan.
Shell for TaskDecomposerCore.

**Methods** (3):
- `__init__(self, fleet_manager)`
- `decompose(self, request)`
- `get_plan_summary(self, steps)`

## Dependencies

**Imports** (6):
- `TaskDecomposerCore.TaskDecomposerCore`
- `json`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
