#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/privilege_escalation_mixin.description.md

# privilege_escalation_mixin

**File**: `src\\core\base\\mixins\\privilege_escalation_mixin.py`  
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
## Source: src-old/core/base/mixins/privilege_escalation_mixin.improvements.md

# Improvements for privilege_escalation_mixin

**File**: `src\\core\base\\mixins\\privilege_escalation_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 66 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `privilege_escalation_mixin_test.py` with pytest tests

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

from __future__ import annotations

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
Module: privilege_escalation_mixin
Privilege escalation mixin for BaseAgent, implementing Windows token manipulation and privilege enabling patterns.
Inspired by ADSyncDump-BOF token impersonation techniques.
"""


import ctypes
import platform
from typing import Any, Optional

from src.core.base.logic.security.privilege_escalation_core import PrivilegeEscalationCore


class PrivilegeEscalationMixin:
    """Mixin providing privilege escalation features for Windows environments."""

    def __init__(self, **kwargs: Any) -> None:
        if platform.system() != "Windows":
            raise RuntimeError("PrivilegeEscalationMixin is only supported on Windows")

        self.privilege_core = PrivilegeEscalationCore()
        self.impersonated_tokens: list = []

    def enable_privilege(self, privilege_name: str) -> bool:
        """Enable a specific Windows privilege."""
        return self.privilege_core.enable_privilege(privilege_name)

    def impersonate_process_token(self, process_id: int) -> bool:
        """Impersonate the token of a target process."""
        success, token_handle = self.privilege_core.impersonate_process_token(process_id)
        if success and token_handle:
            self.impersonated_tokens.append(token_handle)
        return success

    def revert_to_self(self) -> bool:
        """Revert token impersonation."""
        return self.privilege_core.revert_to_self()

    def find_process_by_name(self, process_name: str) -> Optional[int]:
        """Find a process ID by executable name."""
        return self.privilege_core.find_process_by_name(process_name)

    def cleanup_tokens(self) -> None:
        """Clean up any impersonated tokens."""
        for token in self.impersonated_tokens:
            try:
                ctypes.windll.kernel32.CloseHandle(token)
            except:
                pass
        self.impersonated_tokens.clear()
