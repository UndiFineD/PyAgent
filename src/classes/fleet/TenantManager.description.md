# TenantManager

**File**: `src\classes\fleet\TenantManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 50  
**Complexity**: 4 (simple)

## Overview

Manager for multi-tenant workspace isolation.
Simulates Docker-based environment isolation by managing restricted root paths.

## Classes (1)

### `TenantManager`

Manages isolated environments for different users or projects.
Shell for TenantCore.

**Methods** (4):
- `__init__(self, base_root)`
- `create_tenant(self, tenant_id)`
- `get_isolated_path(self, tenant_id, relative_path)`
- `get_tenancy_report(self)`

## Dependencies

**Imports** (8):
- `TenantCore.TenantCore`
- `logging`
- `os`
- `shutil`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
