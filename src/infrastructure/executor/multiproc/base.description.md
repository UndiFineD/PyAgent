# base

**File**: `src\infrastructure\executor\multiproc\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 60  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for base.

## Classes (1)

### `Executor`

**Inherits from**: ABC

Abstract executor base.

**Methods** (7):
- `start(self)`
- `shutdown(self, graceful)`
- `submit(self, func_name)`
- `broadcast(self, func_name)`
- `get_num_workers(self)`
- `is_healthy(self)`
- `get_class(cls, backend)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `src.infrastructure.executor.multiproc.distributed.DistributedExecutor`
- `src.infrastructure.executor.multiproc.future.FutureWrapper`
- `src.infrastructure.executor.multiproc.multiproc_logic.MultiprocExecutor`
- `src.infrastructure.executor.multiproc.types.ExecutorBackend`
- `src.infrastructure.executor.multiproc.uniproc.UniprocExecutor`
- `typing.Any`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
