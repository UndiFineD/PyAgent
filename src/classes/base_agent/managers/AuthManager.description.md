# AuthManager

**File**: `src\classes\base_agent\managers\AuthManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 37  
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

**Imports** (7):
- `logging`
- `src.core.base.core.AuthCore.AuthCore`
- `src.core.base.core.AuthCore.AuthProof`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
