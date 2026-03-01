# MCPAgent

**File**: `src\classes\specialized\MCPAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 109  
**Complexity**: 1 (simple)

## Overview

Agent specializing in Model Context Protocol (MCP) integration.
Acts as a bridge between the PyAgent fleet and external MCP servers.
Inspired by mcp-server-spec-driven-development and awesome-mcp-servers.

## Classes (1)

### `MCPAgent`

**Inherits from**: BaseAgent

Enables the fleet to discover and utilize external tools via the MCP protocol.

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `asyncio`
- `json`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.MCPConnector.MCPConnector`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
