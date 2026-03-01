# tenant_isolation_core

**File**: `src\core\base\logic\core\tenant_isolation_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 80  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for tenant_isolation_core.

## Classes (2)

### `TenantContext`

**Inherits from**: BaseModel

Class TenantContext implementation.

### `TenantIsolationCore`

Handles isolation of agent sessions between different tenants/users.
Patterns harvested from AgentCloud.

**Methods** (5):
- `__init__(self, secret_key)`
- `authorize_session(self, token_payload)`
- `check_access(self, tenant_id, required_scope)`
- `isolate_path(self, base_path, tenant_id)`
- `scrub_metadata(self, metadata, tenant_id)`

## Dependencies

**Imports** (7):
- `os`
- `pydantic.BaseModel`
- `pydantic.Field`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
