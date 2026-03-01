# task_queue_mixin

**File**: `src\core\base\mixins\task_queue_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 151  
**Complexity**: 1 (simple)

## Overview

Task Queue Mixin for BaseAgent.
Provides asynchronous task processing with job queue, inspired by 4o-ghibli-at-home.

## Classes (1)

### `TaskQueueMixin`

Mixin to provide asynchronous task queue capabilities to agents.
Enables background processing of heavy tasks like model inference.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `asyncio`
- `collections.deque`
- `src.core.base.common.models.communication_models.CascadeContext`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
