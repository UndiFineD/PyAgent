# Client

**File**: `src\infrastructure\orchestration\core\distributed\Client.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 21 imports  
**Lines**: 248  
**Complexity**: 11 (moderate)

## Overview

Clients for distributed communication.

## Classes (3)

### `MPClient`

**Inherits from**: Unknown

Client for communicating with worker processes.

Inspired by vLLM's MPClient pattern.
Synchronous interface for multi-process workers.

**Methods** (7):
- `__init__(self, worker_factory, parallel_config)`
- `start(self)`
- `stop(self)`
- `submit(self, request)`
- `get_response(self, timeout)`
- `num_workers(self)`
- `num_pending(self)`

### `AsyncMPClient`

**Inherits from**: Unknown

Async client for communicating with worker processes.

Inspired by vLLM's AsyncMPClient.
Async interface for non-blocking operations.

**Methods** (1):
- `__init__(self, worker_factory, parallel_config)`

### `DPLBAsyncMPClient`

**Inherits from**: Unknown

Data-parallel load-balanced async client.

Inspired by vLLM's dp_lb_pool and DPAsyncMPClient.
Combines coordination with async multi-process execution.

**Methods** (3):
- `__init__(self, worker_factory, parallel_config, load_balancing)`
- `num_engines(self)`
- `num_ready(self)`

## Dependencies

**Imports** (21):
- `Config.EngineIdentity`
- `Config.LoadBalancingStrategy`
- `Config.ParallelConfig`
- `Config.WorkerIdentity`
- `Coordinator.DPCoordinator`
- `Messages.RequestMessage`
- `Messages.ResponseMessage`
- `Worker.BaseWorker`
- `Worker.WorkerProcess`
- `__future__.annotations`
- `asyncio`
- `logging`
- `threading`
- `time`
- `typing.Callable`
- ... and 6 more

---
*Auto-generated documentation*
