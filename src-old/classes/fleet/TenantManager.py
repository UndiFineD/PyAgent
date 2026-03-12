#!/usr/bin/env python3

"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/TenantManager.description.md

# TenantManager

**File**: `src\\classes\fleet\\TenantManager.py`  
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
## Source: src-old/classes/fleet/TenantManager.improvements.md

# Improvements for TenantManager

**File**: `src\\classes\fleet\\TenantManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TenantManager_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""Manager for multi-tenant workspace isolation.
Simulates Docker-based environment isolation by managing restricted root paths.
"""

import logging
import os
from typing import Dict

from .TenantCore import TenantCore


class TenantManager:
    """Manages isolated environments for different users or projects.
    Shell for TenantCore.
    """

    def __init__(self, base_root: str) -> None:
        self.base_root = base_root
        self.tenants_dir = os.path.join(base_root, "tenants")
        self.core = TenantCore()
        if not os.path.exists(self.tenants_dir):
            os.makedirs(self.tenants_dir)
        self.active_tenants: Dict[str, str] = {}

    def create_tenant(self, tenant_id: str) -> str:
        """Creates an isolated workspace for a new tenant."""
        tenant_path = os.path.join(self.tenants_dir, tenant_id)
        if not os.path.exists(tenant_path):
            os.makedirs(tenant_path)
            # Use Core for standardized structure
            for sub_dir in self.core.get_required_dirs():
                os.makedirs(os.path.join(tenant_path, sub_dir), exist_ok=True)
            logging.info(f"TENANT-MGR: Created isolated workspace for {tenant_id}")

        self.active_tenants[tenant_id] = tenant_path
        return tenant_path

    def get_isolated_path(self, tenant_id: str, relative_path: str) -> str:
        """Translates a relative path into the tenant's isolated absolute path."""
        tenant_root = self.active_tenants.get(tenant_id)
        if not tenant_root:
            raise ValueError(f"Tenant {tenant_id} not active.")

        return self.core.validate_and_translate_path(tenant_root, relative_path)

    def get_tenancy_report(self) -> str:
        """Summary of active isolated environments."""
        return f"Tenant Manager: {len(self.active_tenants)} isolated environments established."
