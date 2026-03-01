# orchestrator

**File**: `src\infrastructure\conversation\context\orchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 130  
**Complexity**: 6 (moderate)

## Overview

Tool execution orchestration.

## Classes (1)

### `ToolOrchestrator`

Orchestrate tool execution within conversation.

**Methods** (6):
- `__init__(self, config, tool_handler)`
- `pending_count(self)`
- `has_pending(self)`
- `queue_tool_call(self, call_id, tool_name, arguments)`
- `get_results(self)`
- `clear_completed(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `asyncio`
- `models.ContextConfig`
- `models.ToolExecution`
- `models.ToolExecutionPolicy`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
