# ParallelProcessor

**File**: `src\core\base\common\utils\ParallelProcessor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 71  
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

**Imports** (10):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `concurrent.futures.ThreadPoolExecutor`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `tqdm.tqdm`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
