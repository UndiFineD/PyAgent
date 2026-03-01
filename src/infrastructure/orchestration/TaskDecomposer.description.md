# TaskDecomposer

**File**: `src\infrastructure\orchestration\TaskDecomposer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 46  
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

**Imports** (7):
- `TaskDecomposerCore.TaskDecomposerCore`
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
