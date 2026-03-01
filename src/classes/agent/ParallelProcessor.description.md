# ParallelProcessor

**File**: `src\classes\agent\ParallelProcessor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 55  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for ParallelProcessor.

## Classes (1)

### `ParallelProcessor`

Handles concurrent and parallel execution of tasks across files.

**Methods** (2):
- `__init__(self, max_workers)`
- `process_files_threaded(self, files, worker_func)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `functools`
- `logging`
- `pathlib.Path`
- `tqdm.tqdm`
- `typing.Any`
- `typing.Callable`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
