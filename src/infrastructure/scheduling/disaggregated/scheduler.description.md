# scheduler

**File**: `src\infrastructure\scheduling\disaggregated\scheduler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 20 imports  
**Lines**: 224  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for scheduler.

## Classes (1)

### `DisaggregatedScheduler`

Scheduler for disaggregated prefill-decode inference.

Coordinates request routing between prefill and decode instances.

Inspired by vLLM's disaggregated serving patterns.

**Methods** (8):
- `__init__(self, config)`
- `_create_selector(self, policy)`
- `add_prefill_instance(self, instance)`
- `add_decode_instance(self, instance)`
- `remove_instance(self, instance_id)`
- `schedule_prefill(self, request)`
- `schedule_decode(self, request, prefill_response)`
- `request_finished(self, request_id)`

## Dependencies

**Imports** (20):
- `asyncio`
- `config.DCPConfig`
- `config.InstanceInfo`
- `config.KVTransferParams`
- `config.ScheduledRequest`
- `enums.InstanceRole`
- `enums.SchedulingPolicy`
- `logging`
- `selectors.HashSelector`
- `selectors.InstanceSelector`
- `selectors.LeastLoadedSelector`
- `selectors.RandomSelector`
- `selectors.RoundRobinSelector`
- `time`
- `typing.Any`
- ... and 5 more

---
*Auto-generated documentation*
