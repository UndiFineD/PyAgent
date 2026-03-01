# ToolRegistry

**File**: `src\infrastructure\orchestration\ToolRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 85  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for ToolRegistry.

## Classes (1)

### `ToolRegistry`

Central registry for managing and invoking PyAgent tools across all specialists.

**Methods** (4):
- `__init__(self, fleet)`
- `register_tool(self, owner_name, func, category, priority)`
- `list_tools(self)`
- `get_tool(self, name)`

## Dependencies

**Imports** (12):
- `ToolCore.ToolCore`
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `collections.namedtuple`
- `fleet.FleetManager.FleetManager`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
