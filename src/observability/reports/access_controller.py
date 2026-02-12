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
Access Controller - Manage report access permissions

[Brief Summary]
Simple in-memory controller for granting, revoking and checking report-level permissions using pattern matching and PermissionLevel semantics.

DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.access_controller import AccessController
from src.access_controller.permission_level import PermissionLevel

controller = AccessController()
controller.grant("user1", "*.md", PermissionLevel.READ)
allowed = controller.check("user1", "reports/report.md", PermissionLevel.READ)

WHAT IT DOES:
- Maintains an in-memory list of ReportPermission objects and provides grant, revoke and check operations.
- Uses fnmatch-style patterns (report_pattern) to match report paths and honors permission levels and optional expiry timestamps.
- Normalizes input paths (currently by replacing runs of whitespace with "/") before matching.

WHAT IT SHOULD DO BETTER:
- Path normalization is fragile (replacing whitespace with "/") and should instead use os.path.normpath and explicit separator handling to avoid incorrect matches.
- Permissions storage should support efficient lookup (indexing by user, pattern trees, or compiled regex) and persistence (database or durable store) for production use.
- Add thread-safety, audit logging for grants/revokes, unit tests for edge cases (expired permissions, overlapping patterns), ability to set expirations on grant, and clearer handling of pattern vs. absolute paths.

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

import logging
import re
import time

from src.core.base.lifecycle.version import VERSION

from .permission_level import PermissionLevel
from .report_permission import ReportPermission

__version__ = VERSION


class AccessController:
    """Controller for report access permissions.
    Manages user permissions and access control for reports.
    Attributes:
        permissions: User permissions.
    Example:
        controller=AccessController()
        controller.grant("user1", "*.md", PermissionLevel.READ)
        can_read=controller.check("user1", "report.md", PermissionLevel.READ)
    """

    def __init__(self) -> None:
        """Initialize access controller."""

        self.permissions: list[ReportPermission] = []
        logging.debug("AccessController initialized")

    def grant(
        self,
        user_id: str,
        report_pattern: str,
        level: PermissionLevel,
        granted_by: str = "system",
    ) -> ReportPermission:
        """Grant permission to a user.
        Args:
            user_id: User to grant permission to.
            report_pattern: Pattern for reports.
            level: Permission level.
            granted_by: Who is granting.
        Returns:
            Created permission.
        """

        permission = ReportPermission(
            user_id=user_id,
            report_pattern=report_pattern,
            level=level,
            granted_by=granted_by,
        )
        self.permissions.append(permission)
        return permission

    def revoke(self, user_id: str, report_pattern: str) -> bool:
        """Revoke a permission.
        Args:
            user_id: User ID.
            report_pattern: Pattern to revoke.
        Returns:
            True if revoked.
        """

        for perm in self.permissions:
            if perm.user_id == user_id and perm.report_pattern == report_pattern:
                self.permissions.remove(perm)
                return True
        return False

    def check(self, user_id: str, report_path: str, required_level: PermissionLevel) -> bool:
        """Check if user has permission.
        Args:
            user_id: User to check.
            report_path: Report being accessed.
            required_level: Required permission level.
        Returns:
            True if permitted.
        """

        import fnmatch

        for perm in self.permissions:
            if perm.user_id != user_id:
                continue
            if perm.expires_at and time.time() > perm.expires_at:
                continue
            # Normalize paths for comparison (remove extra spaces)
            normalized_path = re.sub(r"\s+", "/", report_path)
            if fnmatch.fnmatch(normalized_path, perm.report_pattern):
                if perm.level.value >= required_level.value:
                    return True
        return False
"""

from __future__ import annotations

import logging
import re
import time

from src.core.base.lifecycle.version import VERSION

from .permission_level import PermissionLevel
from .report_permission import ReportPermission

__version__ = VERSION


class AccessController:
    """Controller for report access permissions.
    Manages user permissions and access control for reports.
    Attributes:
        permissions: User permissions.
    Example:
        controller=AccessController()
        controller.grant("user1", "*.md", PermissionLevel.READ)
        can_read=controller.check("user1", "report.md", PermissionLevel.READ)
    """

    def __init__(self) -> None:
        """Initialize access controller."""

        self.permissions: list[ReportPermission] = []
        logging.debug("AccessController initialized")

    def grant(
        self,
        user_id: str,
        report_pattern: str,
        level: PermissionLevel,
        granted_by: str = "system",
    ) -> ReportPermission:
        """Grant permission to a user.
        Args:
            user_id: User to grant permission to.
            report_pattern: Pattern for reports.
            level: Permission level.
            granted_by: Who is granting.
        Returns:
            Created permission.
        """

        permission = ReportPermission(
            user_id=user_id,
            report_pattern=report_pattern,
            level=level,
            granted_by=granted_by,
        )
        self.permissions.append(permission)
        return permission

    def revoke(self, user_id: str, report_pattern: str) -> bool:
        """Revoke a permission.
        Args:
            user_id: User ID.
            report_pattern: Pattern to revoke.
        Returns:
            True if revoked.
        """

        for perm in self.permissions:
            if perm.user_id == user_id and perm.report_pattern == report_pattern:
                self.permissions.remove(perm)
                return True
        return False

    def check(self, user_id: str, report_path: str, required_level: PermissionLevel) -> bool:
        """Check if user has permission.
        Args:
            user_id: User to check.
            report_path: Report being accessed.
            required_level: Required permission level.
        Returns:
            True if permitted.
        """

        import fnmatch

        for perm in self.permissions:
            if perm.user_id != user_id:
                continue
            if perm.expires_at and time.time() > perm.expires_at:
                continue
            # Normalize paths for comparison (remove extra spaces)
            normalized_path = re.sub(r"\s+", "/", report_path)
            if fnmatch.fnmatch(normalized_path, perm.report_pattern):
                if perm.level.value >= required_level.value:
                    return True
        return False
