# mcp_tool

**File**: `src\core\integrations\mcp\mcp_tool.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 8 imports  
**Lines**: 132  
**Complexity**: 3 (simple)

## Overview

MCP-based tool registration using official mcp library.
Provides register_tool decorator compatible with mcp.mcp_tool.

## Functions (3)

### `register_tool(name, description)`

Decorator to register a function as a tool using MCP format.
Compatible with mcp.mcp_tool descriptor.

Args:
    name: Optional custom tool name
    description: Optional custom description

### `_generate_mcp_schema(func)`

Generate MCP-compatible JSON schema from function signature.

### `create_mcp_server(name, version)`

Create MCP server with registered tools.

Args:
    name: Server name
    version: Server version

Returns:
    MCP server instance

## Dependencies

**Imports** (8):
- `aenv.core.tool.get_registry`
- `inspect`
- `mcp.server.fastapi.serve_app`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `typing.get_type_hints`

---
*Auto-generated documentation*
