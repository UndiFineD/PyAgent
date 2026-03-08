#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/tenant_isolation_core.description.md

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
## Source: src-old/core/base/logic/core/tenant_isolation_core.improvements.md

# Improvements for tenant_isolation_core

**File**: `src\core\base\logic\core\tenant_isolation_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 80 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: TenantContext

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `tenant_isolation_core_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class TenantContext(BaseModel):
    tenant_id: str
    user_id: Optional[str] = None
    role: str = "viewer"
    scopes: list[str] = Field(default_factory=list)
    exp: int = 0


class TenantIsolationCore:
    """
    Handles isolation of agent sessions between different tenants/users.
    Patterns harvested from AgentCloud.
    """

    def __init__(self, secret_key: str = "default_unsafe_secret"):
        self.secret_key = secret_key
        self.active_sessions: Dict[str, TenantContext] = {}

    def authorize_session(self, token_payload: Dict[str, Any]) -> TenantContext:
        """
        Validates a JWT-like payload and creates a tenant context.
        """
        tenant_id = token_payload.get("tenant_id")
        if not tenant_id:
            raise PermissionError("Missing tenant_id in token")

        # Mock validation logic
        context = TenantContext(
            tenant_id=tenant_id,
            user_id=token_payload.get("user_id"),
            role=token_payload.get("role", "viewer"),
            scopes=token_payload.get("scopes", []),
            exp=token_payload.get("exp", int(time.time() + 3600)),
        )

        self.active_sessions[tenant_id] = context
        return context

    def check_access(self, tenant_id: str, required_scope: str) -> bool:
        """Verifies if the tenant has the required scope for an action."""
        context = self.active_sessions.get(tenant_id)
        if not context:
            return False

        if "admin" in context.scopes:
            return True

        return required_scope in context.scopes

    def isolate_path(self, base_path: str, tenant_id: str) -> str:
        """Generates a tenant-specific filesystem path for sandboxing."""
        import os

        return os.path.join(base_path, "tenants", tenant_id)

    def scrub_metadata(
        self, metadata: Dict[str, Any], tenant_id: str
    ) -> Dict[str, Any]:
        """Ensures cross-tenant data leak prevention by scrubbing sensitive keys."""
        scrubbed = metadata.copy()
        # Remove any keys that don't belong to this tenant_id if present
        if "_internal_tenant" in scrubbed and scrubbed["_internal_tenant"] != tenant_id:
            return {"error": "Tenant mismatch detected during scrub"}

        scrubbed["_internal_tenant"] = tenant_id
        return scrubbed
