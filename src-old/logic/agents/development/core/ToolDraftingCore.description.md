# ToolDraftingCore

**File**: `src\logic\agents\development\core\ToolDraftingCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 61  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ToolDraftingCore.

## Classes (2)

### `ToolDefinition`

Class ToolDefinition implementation.

### `ToolDraftingCore`

Pure logic for agents generating their own OpenAPI tools.
Handles schema drafting, parameter validation, and endpoint mapping.

**Methods** (3):
- `generate_openapi_spec(self, tools)`
- `validate_tool_name(self, name)`
- `map_to_python_stub(self, tool)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
