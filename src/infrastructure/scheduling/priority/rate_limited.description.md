# rate_limited

**File**: `src\infrastructure\scheduling\priority\rate_limited.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 79  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for rate_limited.

## Classes (1)

### `RateLimitedScheduler`

Scheduler with rate limiting per priority level.

**Methods** (4):
- `__init__(self, rates, workers)`
- `submit(self, func, priority)`
- `shutdown(self, wait)`
- `stats(self)`

## Dependencies

**Imports** (10):
- `base.PriorityScheduler`
- `concurrent.futures.Future`
- `enums.TaskPriority`
- `models.TaskStats`
- `threading`
- `time`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `typing.TypeVar`

---
*Auto-generated documentation*
