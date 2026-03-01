# queue

**File**: `src\infrastructure\scheduling\advanced\queue.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 142  
**Complexity**: 9 (moderate)

## Overview

Priority queue implementation for request scheduling.

## Classes (1)

### `PriorityRequestQueue`

Heap-based priority queue for inference requests.

**Methods** (9):
- `__init__(self, enable_starvation_prevention)`
- `_get_priority_score(self, request)`
- `push(self, request)`
- `pop(self)`
- `peek(self)`
- `remove(self, request_id)`
- `_maybe_age_priorities(self)`
- `__len__(self)`
- `__bool__(self)`

## Dependencies

**Imports** (6):
- `config.RequestState`
- `heapq`
- `request.ScheduledRequest`
- `threading`
- `time`
- `typing.Optional`

---
*Auto-generated documentation*
