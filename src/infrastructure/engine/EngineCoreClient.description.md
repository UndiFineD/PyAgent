# EngineCoreClient

**File**: `src\infrastructure\engine\EngineCoreClient.py`  
**Type**: Python Module  
**Summary**: 6 classes, 1 functions, 33 imports  
**Lines**: 416  
**Complexity**: 30 (complex)

## Overview

EngineCoreClient - Client interfaces for engine communication.

Inspired by vLLM's v1/engine/core_client.py - provides various client
implementations for communicating with EngineCore.

## Classes (6)

### `RequestType`

**Inherits from**: Enum

Types of requests to engine core.

### `ClientConfig`

Configuration for engine core clients.

### `EngineCoreClient`

**Inherits from**: ABC

Abstract base class for engine core clients.

Provides interface for adding requests, getting outputs,
and managing engine lifecycle.

**Methods** (10):
- `shutdown(self)`
- `get_output(self)`
- `add_request(self, request)`
- `abort_requests(self, request_ids)`
- `profile(self, is_start)`
- `reset_prefix_cache(self, reset_running_requests, reset_connector)`
- `sleep(self, level)`
- `wake_up(self, tags)`
- `is_sleeping(self)`
- `execute_dummy_batch(self)`

### `InprocClient`

**Inherits from**: EngineCoreClient

In-process client for EngineCore.

Runs the engine in the same process, suitable for single-threaded
or testing scenarios.

**Methods** (6):
- `__init__(self, config, engine_core)`
- `get_output(self)`
- `add_request(self, request)`
- `abort_requests(self, request_ids)`
- `shutdown(self)`
- `profile(self, is_start)`

### `SyncMPClient`

**Inherits from**: EngineCoreClient

Synchronous multiprocess client for EngineCore.

Runs the engine in a background thread with queue-based communication.

**Methods** (7):
- `__init__(self, config)`
- `_run_engine_loop(self)`
- `_handle_request(self, request_type, data)`
- `get_output(self)`
- `add_request(self, request)`
- `abort_requests(self, request_ids)`
- `shutdown(self)`

### `AsyncMPClient`

**Inherits from**: EngineCoreClient

Asynchronous multiprocess client for EngineCore.

Provides async interface with background engine execution.

**Methods** (6):
- `__init__(self, config)`
- `_ensure_output_task(self)`
- `get_output(self)`
- `add_request(self, request)`
- `abort_requests(self, request_ids)`
- `shutdown(self)`

## Functions (1)

### `create_client(client_type, config)`

Factory function to create engine core clients.

Args:
    client_type: Type of client ("inproc", "sync_mp", "async_mp")
    config: Client configuration
    
Returns:
    EngineCoreClient instance

## Dependencies

**Imports** (33):
- `EngineCore.EngineCore`
- `EngineCore.EngineCoreOutputs`
- `EngineCore.EngineCoreProc`
- `EngineCore.MockExecutor`
- `EngineCore.ModelRunnerOutput`
- `EngineCore.Request`
- `EngineCore.SchedulerOutput`
- `EngineCore.SimpleScheduler`
- `OutputProcessor.EngineCoreOutput`
- `OutputProcessor.EngineCoreRequest`
- `OutputProcessor.SamplingParams`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- ... and 18 more

---
*Auto-generated documentation*
