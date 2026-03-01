# async_pipeline_core

**File**: `src\core\base\logic\async_pipeline_core.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 12 imports  
**Lines**: 346  
**Complexity**: 9 (moderate)

## Overview

Async Pipeline Core - Orchestrates asynchronous coding agent pipelines
Based on patterns from agentic-patterns repository (Asynchronous Coding Agent Pipeline)

## Classes (5)

### `TaskStatus`

**Inherits from**: Enum

Status of a pipeline task

### `TaskPriority`

**Inherits from**: Enum

Priority levels for tasks

### `PipelineTask`

Represents a task in the async pipeline

**Methods** (1):
- `__post_init__(self)`

### `PipelineConfig`

Configuration for the async pipeline

### `AsyncPipelineCore`

Orchestrates asynchronous coding agent pipelines
Based on the Asynchronous Coding Agent Pipeline pattern from agentic-patterns

**Methods** (8):
- `__init__(self, config)`
- `register_handler(self, task_type, handler)`
- `get_task_status(self, task_id)`
- `get_all_tasks(self)`
- `get_pending_tasks(self)`
- `get_running_tasks(self)`
- `get_completed_tasks(self)`
- `_check_dependencies(self, task)`

## Dependencies

**Imports** (12):
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `enum.Enum`
- `logging`
- `time`
- `typing.Any`
- `typing.Awaitable`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
