# deadline

**File**: `src\infrastructure\scheduling\priority\deadline.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 127  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for deadline.

## Classes (1)

### `DeadlineScheduler`

Earliest-deadline-first (EDF) scheduler.

Always executes the task with the nearest deadline first.

**Methods** (5):
- `__init__(self, workers)`
- `submit(self, func, deadline_ms, task_id)`
- `_worker_loop(self)`
- `shutdown(self, wait)`
- `stats(self)`

## Dependencies

**Imports** (14):
- `concurrent.futures.Future`
- `concurrent.futures.ThreadPoolExecutor`
- `enums.TaskPriority`
- `enums.TaskState`
- `heapq`
- `models.ScheduledTask`
- `models.TaskStats`
- `threading`
- `time`
- `typing.Callable`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.TypeVar`

---
*Auto-generated documentation*
