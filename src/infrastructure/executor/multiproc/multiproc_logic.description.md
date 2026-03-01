# multiproc_logic

**File**: `src\infrastructure\executor\multiproc\multiproc_logic.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 322  
**Complexity**: 14 (moderate)

## Overview

Python module containing implementation for multiproc_logic.

## Classes (1)

### `MultiprocExecutor`

**Inherits from**: Executor

Multiprocess executor (vLLM MultiprocExecutor equivalent).

**Methods** (14):
- `__init__(self, num_workers, functions, heartbeat_interval, worker_timeout)`
- `register_function(self, name, func)`
- `start(self)`
- `_start_worker(self, worker_id)`
- `_worker_loop(worker_id, task_queue, result_queue, control_queue, functions)`
- `_collect_results(self)`
- `_monitor_workers(self)`
- `_restart_worker(self, worker_id)`
- `shutdown(self, graceful)`
- `submit(self, func_name)`
- ... and 4 more methods

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `multiprocessing`
- `queue`
- `signal`
- `src.infrastructure.executor.multiproc.base.Executor`
- `src.infrastructure.executor.multiproc.future.FutureWrapper`
- `src.infrastructure.executor.multiproc.types.ResultMessage`
- `src.infrastructure.executor.multiproc.types.TaskMessage`
- `src.infrastructure.executor.multiproc.types.WorkerInfo`
- `src.infrastructure.executor.multiproc.types.WorkerState`
- `threading`
- `time`
- `traceback`
- `typing.Any`
- `typing.Callable`
- ... and 3 more

---
*Auto-generated documentation*
