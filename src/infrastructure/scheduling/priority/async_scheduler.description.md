# async_scheduler

**File**: `src\infrastructure\scheduling\priority\async_scheduler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 88  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for async_scheduler.

## Classes (1)

### `AsyncPriorityScheduler`

Async priority scheduler for coroutine-based workloads.

**Methods** (2):
- `__init__(self, max_concurrent)`
- `stats(self)`

## Dependencies

**Imports** (9):
- `asyncio`
- `enums.TaskPriority`
- `models.TaskStats`
- `time`
- `typing.Any`
- `typing.Coroutine`
- `typing.Dict`
- `typing.Optional`
- `typing.TypeVar`

---
*Auto-generated documentation*
