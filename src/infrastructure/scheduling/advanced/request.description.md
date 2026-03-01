# request

**File**: `src\infrastructure\scheduling\advanced\request.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 99  
**Complexity**: 8 (moderate)

## Overview

Request and metrics data structures for scheduling.

## Classes (2)

### `RequestMetrics`

Metrics for a single request.

**Methods** (2):
- `latency_ms(self)`
- `queue_time_ms(self)`

### `ScheduledRequest`

A request scheduled for inference.

**Methods** (6):
- `__post_init__(self)`
- `total_tokens(self)`
- `remaining_tokens(self)`
- `is_preemptible(self)`
- `preempt(self, reason, state)`
- `resume(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `config.PreemptionReason`
- `config.RequestPriority`
- `config.RequestState`
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
