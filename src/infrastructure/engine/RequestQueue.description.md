# RequestQueue

**File**: `src\infrastructure\engine\RequestQueue.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 13 imports  
**Lines**: 42  
**Complexity**: 0 (simple)

## Overview

Facade for Request Queue.
Delegates to modularized sub-packages in src/infrastructure/engine/request_queue/.

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `request_queue.DeadlineQueue`
- `request_queue.FCFSQueue`
- `request_queue.FairQueue`
- `request_queue.MLFQueue`
- `request_queue.PriorityQueue`
- `request_queue.QueuedRequest`
- `request_queue.RequestPriority`
- `request_queue.RequestQueue`
- `request_queue.RequestQueueManager`
- `request_queue.RequestStatus`
- `request_queue.SchedulingPolicy`
- `request_queue.create_request_queue`

---
*Auto-generated documentation*
