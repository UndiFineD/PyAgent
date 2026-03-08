# AuthManager

**File**: `src\core\base\managers\AuthManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 38  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for AuthManager.

## Classes (1)

### `AuthManager`

Shell for agent authentication and access control.
Wraps AuthCore with stateful session management.

**Methods** (3):
- `__init__(self)`
- `initiate_auth(self, agent_id)`
- `authenticate(self, agent_id, proof)`

## Dependencies

**Imports** (4):
- `logging`
- `src.core.base.core.AuthCore.AuthCore`
- `time`
- `typing.Dict`

---
*Auto-generated documentation*
