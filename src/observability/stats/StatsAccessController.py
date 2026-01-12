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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



from typing import Dict



































class StatsAccessController:
    """Controls access to stats."""
    def __init__(self) -> None:
        self.permissions: Dict[str, Dict[str, str]] = {}

    def grant(self, user: str, resource_pattern: str, level: str = "read") -> None:
        """Grant access level for a resource pattern.

        Compatibility: tests call `grant(user, pattern, level='read'|'write')`.
        """
        self.grant_access(user, resource_pattern, level)

    def can_access(self, user: str, resource: str, required_level: str = "read") -> bool:
        """Check whether user can access resource at required level."""
        import fnmatch

        if user not in self.permissions:
            return False

        required = required_level.lower()
        # Treat "write" as superset of "read".
        for pattern, granted_level in self.permissions[user].items():
            if not fnmatch.fnmatch(resource, pattern):
                continue
            granted = granted_level.lower()
            if required == "read":
                if granted in ("read", "write"):
                    return True
            elif required == "write":
                if granted == "write":
                    return True
            else:
                # Unknown required level: fall back to exact match.
                if granted == required:
                    return True
        return False

    def grant_access(self, user: str, resource: str, permission: str) -> None:
        """Grant access to user."""
        if user not in self.permissions:
            self.permissions[user] = {}
        self.permissions[user][resource] = permission

    def has_access(self, user: str, resource: str) -> bool:
        """Check if user has access."""
        return user in self.permissions and resource in self.permissions[user]
