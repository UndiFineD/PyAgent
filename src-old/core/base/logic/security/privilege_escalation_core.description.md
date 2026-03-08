# privilege_escalation_core

**File**: `src\core\base\logic\security\privilege_escalation_core.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 5 imports  
**Lines**: 205  
**Complexity**: 5 (moderate)

## Overview

Module: privilege_escalation_core
Core logic for Windows privilege escalation operations.
Implements token manipulation and privilege enabling patterns from ADSyncDump-BOF.

## Classes (5)

### `LUID`

**Inherits from**: Structure

Class LUID implementation.

### `LUID_AND_ATTRIBUTES`

**Inherits from**: Structure

Class LUID_AND_ATTRIBUTES implementation.

### `TOKEN_PRIVILEGES`

**Inherits from**: Structure

Class TOKEN_PRIVILEGES implementation.

### `PROCESSENTRY32`

**Inherits from**: Structure

Class PROCESSENTRY32 implementation.

### `PrivilegeEscalationCore`

Core class for Windows privilege escalation operations.

**Methods** (5):
- `__init__(self)`
- `enable_privilege(self, privilege_name)`
- `find_process_by_name(self, process_name)`
- `impersonate_process_token(self, process_id)`
- `revert_to_self(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `ctypes`
- `ctypes.wintypes`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
