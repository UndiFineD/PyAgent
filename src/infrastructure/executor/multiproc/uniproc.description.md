# uniproc

**File**: `src\infrastructure\executor\multiproc\uniproc.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 62  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for uniproc.

## Classes (1)

### `UniprocExecutor`

**Inherits from**: Executor

Single-process executor for debugging and simple use cases.

**Methods** (8):
- `__init__(self, functions)`
- `register_function(self, name, func)`
- `start(self)`
- `shutdown(self, graceful)`
- `submit(self, func_name)`
- `broadcast(self, func_name)`
- `get_num_workers(self)`
- `is_healthy(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `src.infrastructure.executor.multiproc.base.Executor`
- `src.infrastructure.executor.multiproc.future.FutureWrapper`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
