# APICore

**File**: `src\classes\api\APICore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 75  
**Complexity**: 3 (simple)

## Overview

APICore logic for fleet communication.
Pure logic for OpenAPI spec generation and tool contract validation.

## Classes (1)

### `APICore`

Class APICore implementation.

**Methods** (3):
- `__init__(self, version)`
- `build_openapi_json(self, tool_definitions)`
- `validate_tool_contract(self, spec)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `json`
- `src.core.base.version.SDK_VERSION`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
