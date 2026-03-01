# AuthManagers

**File**: `src\classes\base_agent\managers\AuthManagers.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 11 imports  
**Lines**: 103  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for AuthManagers.

## Classes (2)

### `AuthenticationManager`

Manager for authentication methods.

**Methods** (6):
- `__init__(self, config)`
- `get_headers(self)`
- `_get_oauth_token(self)`
- `refresh_token(self)`
- `set_custom_header(self, key, value)`
- `validate(self)`

### `AuthManager`

Manages authentication.

**Methods** (3):
- `set_method(self, method)`
- `add_custom_header(self, header, value)`
- `get_headers(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `base64`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `src.core.base.models.AuthConfig`
- `src.core.base.models.AuthMethod`
- `src.core.base.models._empty_dict_str_str`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
