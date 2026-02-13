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
Access.py - Stats Access Control

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Instantiate StatsAccessController(), call grant(user, pattern, level="read") to assign permissions and can_access(user, resource, required_level="read") to check access.

WHAT IT DOES:
Provides a minimal, pattern-based stats access controller using fnmatch with a permissions dict mapping users to pattern→level entries and supports read/write checks.

WHAT IT SHOULD DO BETTER:
Validate inputs and permission levels, provide explicit deny rules and logging, use enums for levels, add persistence and thread-safety, support more granular and hierarchical permission semantics, and include unit tests and documentation for edge cases.

FILE CONTENT SUMMARY:
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
