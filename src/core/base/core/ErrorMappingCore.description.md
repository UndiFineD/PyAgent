# ErrorMappingCore

**File**: `src\core\base\core\ErrorMappingCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 71  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ErrorMappingCore.

## Classes (1)

### `ErrorMappingCore`

Pure logic for mapping system exceptions to standardized PA-xxxx error codes.
Targeted for Rust conversion to ensure consistency across the swarm.

**Methods** (3):
- `get_code(cls, exception_name)`
- `get_troubleshooting_link(cls, error_code)`
- `describe_error(cls, error_code)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `typing.Dict`

---
*Auto-generated documentation*
