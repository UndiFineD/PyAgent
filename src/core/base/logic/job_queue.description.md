# job_queue

**File**: `src\core\base\logic\job_queue.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 251  
**Complexity**: 10 (moderate)

## Overview

In-Memory Job Queue System
==========================

Inspired by 4o-ghibli-at-home's job queue pattern.
Provides thread-safe job queuing with background processing and TTL cleanup.

## Classes (1)

### `JobQueue`

Thread-safe in-memory job queue with background processing.

Features:
- Thread-safe job queuing and processing
- Background worker threads
- Job status tracking
- TTL-based cleanup
- Configurable queue size limits

**Methods** (10):
- `__init__(self, max_queue_size, job_ttl_seconds, cleanup_interval_seconds, num_workers)`
- `set_job_processor(self, processor)`
- `start(self)`
- `stop(self)`
- `submit_job(self, job_data)`
- `get_job_status(self, job_id)`
- `cancel_job(self, job_id)`
- `_worker_loop(self)`
- `_cleanup_loop(self)`
- `get_stats(self)`

## Dependencies

**Imports** (10):
- `collections.deque`
- `datetime.datetime`
- `datetime.timedelta`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
