# BatchManagers

**File**: `src\classes\base_agent\managers\BatchManagers.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 15 imports  
**Lines**: 140  
**Complexity**: 13 (moderate)

## Overview

Python module containing implementation for BatchManagers.

## Classes (2)

### `BatchRequest`

Request in a batch processing queue.

**Methods** (4):
- `__init__(self, file_path, prompt, priority, callback, max_size)`
- `add(self, item)`
- `size(self)`
- `execute(self, processor)`

### `RequestBatcher`

Batch processor for multiple file requests.

**Methods** (9):
- `__init__(self, batch_size, max_concurrent, recorder)`
- `add_request(self, request)`
- `add_requests(self, requests)`
- `get_queue_size(self)`
- `clear_queue(self)`
- `_sort_by_priority(self)`
- `process_batch(self, agent_factory)`
- `process_all(self, agent_factory)`
- `get_stats(self)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `agent.BaseAgent`
- `collections.abc.Callable`
- `logging`
- `pathlib.Path`
- `src.core.base.models.BatchResult`
- `src.core.base.models.FilePriority`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
