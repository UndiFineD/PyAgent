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
Access.py module.
"""
# Access control for stats.

from __future__ import annotations

import fnmatch


class StatsAccessController:
    """Controls access to stats."""

    def __init__(self) -> None:
        self.permissions: dict[str, dict[str, str]] = {}

    def grant(self, user: str, pattern: str, level: str = "read") -> None:
        self.permissions.setdefault(user, {})[pattern] = level

    def can_access(self, user: str, resource: str, required_level: str = "read") -> bool:
        if user not in self.permissions:
            return False
        req = required_level.lower()
        for pat, granted in self.permissions[user].items():
            if fnmatch.fnmatch(resource, pat):
                g = granted.lower()
                if req == "read" and g in ("read", "write"):
                    return True
                if req == "write" and g == "write":
                    return True
        return False
