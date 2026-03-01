# factory

**File**: `src\infrastructure\executor\multiproc\factory.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 27  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for factory.

## Classes (1)

### `ExecutorFactory`

Factory for creating executors.

**Methods** (1):
- `create(backend, num_workers, functions)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `src.infrastructure.executor.multiproc.base.Executor`
- `src.infrastructure.executor.multiproc.distributed.DistributedExecutor`
- `src.infrastructure.executor.multiproc.multiproc_logic.MultiprocExecutor`
- `src.infrastructure.executor.multiproc.types.ExecutorBackend`
- `src.infrastructure.executor.multiproc.uniproc.UniprocExecutor`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`

---
*Auto-generated documentation*
