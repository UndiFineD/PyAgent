# distributed

**File**: `src\infrastructure\executor\multiproc\distributed.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 71  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for distributed.

## Classes (1)

### `DistributedExecutor`

**Inherits from**: Executor

Distributed executor for multi-node setups.

**Methods** (8):
- `__init__(self, world_size, rank, local_size, functions)`
- `start(self)`
- `shutdown(self, graceful)`
- `submit(self, func_name)`
- `broadcast(self, func_name)`
- `get_num_workers(self)`
- `is_healthy(self)`
- `is_leader(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `src.infrastructure.executor.multiproc.base.Executor`
- `src.infrastructure.executor.multiproc.future.FutureWrapper`
- `src.infrastructure.executor.multiproc.multiproc_logic.MultiprocExecutor`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
