# asynchronous_agent_pipeline_core

**File**: `src\core\base\logic\core\asynchronous_agent_pipeline_core.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 16 imports  
**Lines**: 359  
**Complexity**: 4 (simple)

## Overview

Asynchronous Agent Pipeline Core

Inspired by agentic-patterns repository asynchronous coding agent pipeline.
Implements decoupled inference, tool execution, and learning for parallel processing.

## Classes (4)

### `ToolCall`

Represents a tool call request

### `ToolResult`

Result from tool execution

### `Trajectory`

Complete trajectory from state to reward

### `AsynchronousAgentPipelineCore`

Core implementing asynchronous agent pipeline pattern.

Decouples inference, tool execution, and learning into parallel components
communicating via queues to eliminate compute bubbles.

**Methods** (4):
- `__init__(self, max_workers, queue_size)`
- `register_tool(self, name, tool_func)`
- `_compute_reward(self, state, tool_call, tool_result, execution_time)`
- `get_statistics(self)`

## Dependencies

**Imports** (16):
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `datetime.datetime`
- `json`
- `logging`
- `queue.Queue`
- `threading`
- `time`
- `typing.Any`
- `typing.Awaitable`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
