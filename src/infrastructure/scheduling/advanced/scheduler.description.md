# scheduler

**File**: `src\infrastructure\scheduling\advanced\scheduler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 2 functions, 14 imports  
**Lines**: 332  
**Complexity**: 15 (moderate)

## Overview

Advanced request scheduler coordinator.

## Classes (1)

### `AdvancedRequestScheduler`

Advanced request scheduler with priority and preemption.

**Methods** (13):
- `__init__(self, config)`
- `add_request(self, prompt, priority, max_tokens, deadline, request_id, prompt_tokens)`
- `schedule(self)`
- `_should_preempt(self, incoming, available_budget)`
- `_preempt_for_request(self, incoming)`
- `_preempt_request(self, request_id, reason, saved_state)`
- `preempt_request(self, request_id, reason, saved_state)`
- `resume_request(self, request_id)`
- `complete_request(self, request_id, generated_tokens)`
- `abort_request(self, request_id)`
- ... and 3 more methods

## Functions (2)

### `create_scheduler(max_tokens, max_requests, preemption)`

Create a scheduler with common settings.

### `priority_from_string(s)`

Convert string to RequestPriority.

## Dependencies

**Imports** (14):
- `config.PreemptionReason`
- `config.RequestPriority`
- `config.RequestState`
- `config.SchedulerConfig`
- `queue.PriorityRequestQueue`
- `request.RequestMetrics`
- `request.ScheduledRequest`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
