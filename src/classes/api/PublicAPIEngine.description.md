# PublicAPIEngine

**File**: `src\classes\api\PublicAPIEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 41  
**Complexity**: 3 (simple)

## Overview

Public API Engine for PyAgent.
Generates OpenAPI/Swagger specs and handles external tool integration.

## Classes (1)

### `PublicAPIEngine`

Manages the external interface for third-party integrations.
Shell for APICore.

**Methods** (3):
- `__init__(self, fleet_manager)`
- `generate_openapi_spec(self)`
- `register_external_tool(self, tool_spec)`

## Dependencies

**Imports** (6):
- `APICore.APICore`
- `json`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
