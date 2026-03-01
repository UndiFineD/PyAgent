# base

**File**: `src\infrastructure\mcp_tools\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 98  
**Complexity**: 7 (moderate)

## Overview

Base MCP tool server abstraction.

## Classes (1)

### `MCPToolServer`

**Inherits from**: ABC

Abstract base class for MCP tool servers.

**Methods** (7):
- `__init__(self, config)`
- `name(self)`
- `session(self)`
- `tools(self)`
- `get_tool(self, name)`
- `_apply_namespace_filter(self, tools)`
- `_create_session(self)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `models.MCPServerConfig`
- `models.MCPSession`
- `models.SessionState`
- `models.ToolCall`
- `models.ToolResult`
- `models.ToolSchema`
- `time`
- `typing.Any`
- `typing.AsyncIterator`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
