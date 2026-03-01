# Executor

**File**: `src\infrastructure\orchestration\core\distributed\Executor.py`  
**Type**: Python Module  
**Summary**: 2 classes, 5 functions, 15 imports  
**Lines**: 150  
**Complexity**: 8 (moderate)

## Overview

Executor interface and implementations for distributed execution.

## Classes (2)

### `DistributedExecutor`

**Inherits from**: ABC

Abstract interface for distributed execution.

Inspired by vLLM's ExecutorBase.

**Methods** (1):
- `is_ready(self)`

### `MultiProcessExecutor`

**Inherits from**: DistributedExecutor

Multi-process distributed executor.

Implements distributed execution using multiprocessing.

**Methods** (2):
- `__init__(self, worker_factory, parallel_config, load_balancing)`
- `is_ready(self)`

## Functions (5)

### `create_distributed_executor(worker_factory, parallel_config, load_balancing)`

Create a distributed executor.

Args:
    worker_factory: Factory function for creating workers.
    parallel_config: Parallel configuration.
    load_balancing: Load balancing strategy.

Returns:
    Configured distributed executor.

### `get_dp_rank()`

Get current data parallel rank from environment.

### `get_dp_size()`

Get data parallel world size from environment.

### `get_tp_rank()`

Get current tensor parallel rank from environment.

### `get_tp_size()`

Get tensor parallel world size from environment.

## Dependencies

**Imports** (15):
- `Client.DPLBAsyncMPClient`
- `Config.LoadBalancingStrategy`
- `Config.ParallelConfig`
- `Config.WorkerIdentity`
- `Messages.RequestMessage`
- `Messages.ResponseMessage`
- `Worker.BaseWorker`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `os`
- `typing.Any`
- `typing.Callable`
- `typing.Optional`

---
*Auto-generated documentation*
