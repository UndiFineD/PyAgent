# base

**File**: `src\infrastructure\scheduling\priority\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 276  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for base.

## Classes (1)

### `PriorityScheduler`

Priority-based task scheduler with deadline support.

Features:
- Priority-based scheduling (CRITICAL to IDLE)
- Deadline-aware execution
- Timeout handling
- Work stealing between priority levels
- Statistics tracking

**Methods** (12):
- `__init__(self, workers, max_queue_size, enable_work_stealing)`
- `submit(self, func, priority, deadline_ms, timeout_ms, task_id)`
- `_worker_loop(self, worker_id)`
- `_get_next_task(self)`
- `_execute_task(self, task)`
- `_execute_with_timeout(self, func, timeout)`
- `_handle_timeout(self, task)`
- `cancel(self, task_id)`
- `shutdown(self, wait, timeout)`
- `pending_count(self)`
- ... and 2 more methods

## Dependencies

**Imports** (15):
- `concurrent.futures.Future`
- `concurrent.futures.ThreadPoolExecutor`
- `enums.TaskPriority`
- `enums.TaskState`
- `heapq`
- `models.ScheduledTask`
- `models.TaskStats`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TypeVar`

---
*Auto-generated documentation*
