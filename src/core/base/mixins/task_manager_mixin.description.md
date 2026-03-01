# task_manager_mixin

**File**: `src\core\base\mixins\task_manager_mixin.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 282  
**Complexity**: 7 (moderate)

## Overview

Task Management Mixin for BaseAgent.
Provides structured task tracking and management, inspired by Adorable's todo tool.

## Classes (2)

### `TaskItem`

Represents a single task item.

**Methods** (4):
- `to_dict(self)`
- `from_dict(cls, data)`
- `complete(self)`
- `reset(self)`

### `TaskManagerMixin`

Mixin providing structured task management capabilities.
Inspired by Adorable's todo tool for tracking agent tasks and workflows.

**Methods** (3):
- `__init__(self)`
- `_load_tasks(self)`
- `_save_tasks(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.common.models.communication_models.CascadeContext`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
