# MCPConnector

**File**: `src\classes\fleet\MCPConnector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 117  
**Complexity**: 6 (moderate)

## Overview

Low-level connector for Model Context Protocol (MCP) servers using stdio transport.

## Classes (1)

### `MCPConnector`

Manages the lifecycle and JSON-RPC communication with an MCP server.

**Methods** (6):
- `__init__(self, name, command, env, recorder)`
- `_record(self, action, result)`
- `start(self)`
- `_read_stderr(self)`
- `call(self, method, params, timeout)`
- `stop(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `src.core.base.version.VERSION`
- `subprocess`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
