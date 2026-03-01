# SecurityAuditManager

**File**: `src\classes\coder\SecurityAuditManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 43  
**Complexity**: 4 (simple)

## Overview

Security auditor for the fleet.
Handles certificate rotation and security policy enforcement.

## Classes (1)

### `SecurityAuditManager`

Manages fleet security including certificates and access control.

**Methods** (4):
- `__init__(self)`
- `rotate_certificates(self, fleet_id)`
- `audit_agent_permissions(self, agent_id)`
- `enforce_policy(self, command)`

## Dependencies

**Imports** (6):
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `uuid`

---
*Auto-generated documentation*
