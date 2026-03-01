# Worker

**File**: `src\infrastructure\orchestration\core\distributed\Worker.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 15 imports  
**Lines**: 214  
**Complexity**: 12 (moderate)

## Overview

Distributed worker implementations.

## Classes (2)

### `BaseWorker`

**Inherits from**: ABC

Abstract base class for distributed workers.

Workers receive requests, process them, and return results.

**Methods** (5):
- `__init__(self, identity)`
- `initialize(self)`
- `process(self, request)`
- `shutdown(self)`
- `get_metrics(self)`

### `WorkerProcess`

Wrapper for a worker running in a subprocess.

Inspired by vLLM's CoreEngineProc.

**Methods** (7):
- `__init__(self, worker_id, worker_factory, engine_id, rank, world_size)`
- `start(self)`
- `_worker_main(worker_id, worker_factory, engine_id, rank, world_size, request_queue, response_queue, control_queue)`
- `stop(self, timeout)`
- `submit(self, request)`
- `get_response(self, timeout)`
- `is_alive(self)`

## Dependencies

**Imports** (15):
- `Config.WorkerIdentity`
- `Config.WorkerState`
- `Messages.ControlMessage`
- `Messages.MetricsMessage`
- `Messages.RequestMessage`
- `Messages.ResponseMessage`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `multiprocessing`
- `queue`
- `time`
- `typing.Callable`
- `typing.Optional`

---
*Auto-generated documentation*
