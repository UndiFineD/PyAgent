# future

**File**: `src\infrastructure\executor\multiproc\future.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 77  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for future.

## Classes (1)

### `FutureWrapper`

**Inherits from**: Unknown

Future wrapper for async task results.

**Methods** (8):
- `__init__(self, task_id)`
- `set_result(self, result)`
- `set_exception(self, error)`
- `result(self, timeout)`
- `done(self)`
- `cancel(self)`
- `cancelled(self)`
- `add_done_callback(self, callback)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- `typing.List`
- `typing.Optional`
- `typing.TypeVar`

---
*Auto-generated documentation*
