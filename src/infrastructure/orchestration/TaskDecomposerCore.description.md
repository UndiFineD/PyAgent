# TaskDecomposerCore

**File**: `src\infrastructure\orchestration\TaskDecomposerCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 111  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for TaskDecomposerCore.

## Classes (2)

### `PlanStep`

Class PlanStep implementation.

### `TaskDecomposerCore`

Pure logic for task decomposition.
Handles heuristic-based planning and plan summarization.

**Methods** (3):
- `generate_plan(self, request)`
- `_to_dict(self, step)`
- `summarize_plan(self, steps)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
