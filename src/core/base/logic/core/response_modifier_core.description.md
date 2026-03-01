# response_modifier_core

**File**: `src\core\base\logic\core\response_modifier_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 10 imports  
**Lines**: 291  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for response_modifier_core.

## Classes (3)

### `ResponseModificationRule`

Rule for modifying HTTP responses

### `ModifiedResponse`

Container for modified response data

### `ResponseModifierCore`

**Inherits from**: BaseCore

HTTP Response Modifier Core for security testing and analysis.

Provides capabilities to modify HTTP response codes and content
for testing purposes, similar to Burp Suite extensions.
Useful for bypassing client-side validations and testing error handling.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (10):
- `asyncio`
- `dataclasses.dataclass`
- `re`
- `src.core.base.logic.core.base_core.BaseCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
