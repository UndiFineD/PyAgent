# privilege_escalation_mixin

**File**: `src\core\base\mixins\privilege_escalation_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 66  
**Complexity**: 6 (moderate)

## Overview

Module: privilege_escalation_mixin
Privilege escalation mixin for BaseAgent, implementing Windows token manipulation and privilege enabling patterns.
Inspired by ADSyncDump-BOF token impersonation techniques.

## Classes (1)

### `PrivilegeEscalationMixin`

Mixin providing privilege escalation features for Windows environments.

**Methods** (6):
- `__init__(self)`
- `enable_privilege(self, privilege_name)`
- `impersonate_process_token(self, process_id)`
- `revert_to_self(self)`
- `find_process_by_name(self, process_name)`
- `cleanup_tokens(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `ctypes`
- `platform`
- `src.core.base.logic.security.privilege_escalation_core.PrivilegeEscalationCore`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
