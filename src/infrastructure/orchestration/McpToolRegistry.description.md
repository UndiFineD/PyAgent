# McpToolRegistry

**File**: `src\infrastructure\orchestration\McpToolRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 57  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for McpToolRegistry.

## Classes (1)

### `McpToolRegistry`

**Inherits from**: ToolRegistry

Registry specialized for Model Context Protocol (MCP) tools.

**Methods** (2):
- `__init__(self, fleet)`
- `register_mcp_server(self, server_name, tools, call_handler)`

## Dependencies

**Imports** (8):
- `ToolRegistry.ToolRegistry`
- `__future__.annotations`
- `fleet.FleetManager.FleetManager`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
