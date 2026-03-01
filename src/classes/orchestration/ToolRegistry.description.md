# ToolRegistry

**File**: `src\classes\orchestration\ToolRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 65  
**Complexity**: 5 (moderate)

## Overview

Central registry for all agent tools and capabilities.

## Classes (1)

### `ToolRegistry`

A registry that allows agents to discover and invoke tools across the fleet.
Shell for ToolCore.

**Methods** (5):
- `__new__(cls)`
- `register_tool(self, owner_name, func, category, priority)`
- `list_tools(self, category)`
- `get_tool(self, name)`
- `call_tool(self, name)`

## Dependencies

**Imports** (10):
- `ToolCore.ToolCore`
- `ToolCore.ToolMetadata`
- `inspect`
- `logging`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
