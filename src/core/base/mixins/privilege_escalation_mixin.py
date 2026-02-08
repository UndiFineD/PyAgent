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
Module: privilege_escalation_mixin
Privilege escalation mixin for BaseAgent, implementing Windows token manipulation and privilege enabling patterns.
Inspired by ADSyncDump-BOF token impersonation techniques.
"""

from __future__ import annotations

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
            except Exception:
                pass
        self.impersonated_tokens.clear()
