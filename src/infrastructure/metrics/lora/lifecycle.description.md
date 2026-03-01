# lifecycle

**File**: `src\infrastructure\metrics\lora\lifecycle.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 267  
**Complexity**: 20 (complex)

## Overview

LoRA Request Lifecycle - Detailed tracking of per-request events and timing.

## Classes (2)

### `RequestLifecycle`

Enhanced request lifecycle tracking.

**Methods** (13):
- `__init__(self, request_id, prompt_tokens, max_tokens, lora_adapter)`
- `_record_event(self, event_type, data)`
- `status(self)`
- `transition_to(self, new_status)`
- `record_token(self)`
- `finish(self, reason)`
- `time_to_first_token(self)`
- `total_latency(self)`
- `tokens_generated(self)`
- `inter_token_latency(self)`
- ... and 3 more methods

### `RequestLifecycleManager`

Manager for request lifecycles.

**Methods** (7):
- `__init__(self, max_completed)`
- `create(self, request_id, prompt_tokens, max_tokens, lora_adapter)`
- `get(self, request_id)`
- `finish(self, request_id, reason)`
- `get_active_count(self)`
- `get_completed_count(self)`
- `get_aggregate_stats(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `src.infrastructure.metrics.lora.types.RequestStatus`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
