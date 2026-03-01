# models

**File**: `src\infrastructure\mcp_tools\models.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 12 imports  
**Lines**: 204  
**Complexity**: 9 (moderate)

## Overview

MCP-related data models and enums.

## Classes (8)

### `MCPServerType`

**Inherits from**: Enum

MCP server connection types.

### `ToolStatus`

**Inherits from**: Enum

Tool execution status.

### `SessionState`

**Inherits from**: Enum

MCP session state.

### `MCPServerConfig`

MCP server configuration.

**Methods** (1):
- `to_dict(self)`

### `ToolSchema`

Tool schema definition.

**Methods** (3):
- `to_openai_format(self)`
- `full_name(self)`
- `to_dict(self)`

### `ToolCall`

Tool call request.

**Methods** (1):
- `from_openai_format(cls, data)`

### `ToolResult`

Tool execution result.

**Methods** (2):
- `to_openai_format(self)`
- `is_success(self)`

### `MCPSession`

MCP session information.

**Methods** (2):
- `is_ready(self)`
- `uptime_seconds(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `uuid`

---
*Auto-generated documentation*
