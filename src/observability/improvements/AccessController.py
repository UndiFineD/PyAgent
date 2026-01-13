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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Dict, List

__version__ = VERSION

class AccessController:
    """Tracks per-improvement permissions and roles."""

    def __init__(self) -> None:
        self.permissions: dict[str, dict[str, set[str]]] = {}
        self._roles: dict[str, list[str]] = {}
        self._assigned_roles: dict[str, dict[str, str]] = {}

    def define_role(self, role: str, permissions: list[str]) -> None:
        self._roles[role] = list(permissions)

    def assign_role(self, improvement_id: str, user: str, role: str) -> None:
        self._assigned_roles.setdefault(improvement_id, {})[user] = role

    def grant(self, improvement_id: str, user: str, level: str) -> None:
        self.permissions.setdefault(improvement_id, {}).setdefault(user, set()).add(level)

    def can_access(self, improvement_id: str, user: str, level: str) -> bool:
        direct = level in self.permissions.get(improvement_id, {}).get(user, set())
        if direct:
            return True
        role = self._assigned_roles.get(improvement_id, {}).get(user)
        if role and role in self._roles:
            return level in self._roles[role]
        return False