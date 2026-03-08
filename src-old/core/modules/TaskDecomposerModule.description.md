# TaskDecomposerModule

**File**: `src\core\modules\TaskDecomposerModule.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 116  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for TaskDecomposerModule.

## Classes (2)

### `PlanStep`

Class PlanStep implementation.

### `TaskDecomposerModule`

**Inherits from**: BaseModule

Consolidated core module for task decomposition.
Migrated from TaskDecomposerCore.

**Methods** (5):
- `initialize(self)`
- `execute(self, request)`
- `_to_dict(self, step)`
- `summarize_plan(self, steps)`
- `shutdown(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
