# utilities

**File**: `src\classes\base_agent\utilities.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 18 imports  
**Lines**: 211  
**Complexity**: 3 (simple)

## Overview

Utility classes for BaseAgent framework.

## Functions (3)

### `setup_logging(verbosity_arg)`

Configure logging based on verbosity level.

### `as_tool(priority, category)`

Decorator to mark a method as a tool for the ToolRegistry.
Automatically records tool interactions to the fleet context shards for autonomous learning.
Can be used as @as_tool or @as_tool(priority=10).

### `create_main_function(agent_class, description, context_help)`

Create a main function for an agent class.

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `agent.BaseAgent`
- `argparse`
- `collections.abc.Callable`
- `functools.wraps`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.logic.strategies.plan_executor`
- `sys`
- `time`
- `typing.Any`
- `typing.Optional`
- ... and 3 more

---
*Auto-generated documentation*
