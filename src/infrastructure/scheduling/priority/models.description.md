# models

**File**: `src\infrastructure\scheduling\priority\models.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 75  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for models.

## Classes (2)

### `TaskStats`

Statistics for task execution.

**Methods** (3):
- `avg_wait_time_ms(self)`
- `avg_exec_time_ms(self)`
- `to_dict(self)`

### `ScheduledTask`

**Inherits from**: Unknown

A task scheduled for execution.

**Methods** (1):
- `is_expired(self)`

## Dependencies

**Imports** (12):
- `concurrent.futures.Future`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.TaskPriority`
- `enums.TaskState`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generic`
- `typing.Optional`
- `typing.TypeVar`

---
*Auto-generated documentation*
