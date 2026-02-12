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
Report Permission - Data model for report access control

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate to represent a user's permission for matching reports:
  rp = ReportPermission(user_id="alice", report_pattern="reports/*.json", level=PermissionLevel.READ, granted_by="admin", expires_at=None)
- Use as a serializable dataclass for persistence or for in-memory permission checks.
- Prefer converting expires_at (float) to a datetime when evaluating expiry.

WHAT IT DOES:
- Provides a lightweight dataclass (ReportPermission) that models access to reports via a glob-style report_pattern, associated user_id, permission level, grantor, and optional expiration timestamp.
- Centralizes the permission shape used by reporting code and permission-checking logic.

WHAT IT SHOULD DO BETTER:
- Replace expires_at: float | None with timezone-aware datetime to avoid epoch/timezone ambiguity.
- Add validation (e.g., ensure non-empty user_id, valid glob/pattern sanity, level is PermissionLevel) and factory methods for common cases.
- Implement helper methods: is_expired(), matches_report(path), to_dict()/from_dict() for stable serialization.
- Add unit tests and clearer module-level docstring describing intended integration with RBAC or report-generation flows.

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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .permission_level import PermissionLevel

__version__: str = VERSION


@dataclass
class ReportPermission:
    """Permission for report access.
    Attributes:
        user_id: User identifier.
        report_pattern: Glob pattern for reports.
        level: Permission level.
        granted_by: Who granted permission.
        expires_at: Expiration timestamp.
    """

    user_id: str
    report_pattern: str
    level: PermissionLevel = PermissionLevel.READ
    granted_by: str = ""
    expires_at: float | None = None
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .permission_level import PermissionLevel

__version__: str = VERSION


@dataclass
class ReportPermission:
    """Permission for report access.
    Attributes:
        user_id: User identifier.
        report_pattern: Glob pattern for reports.
        level: Permission level.
        granted_by: Who granted permission.
        expires_at: Expiration timestamp.
    """

    user_id: str
    report_pattern: str
    level: PermissionLevel = PermissionLevel.READ
    granted_by: str = ""
    expires_at: float | None = None
