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
from src.core.base.Version import VERSION
from .AuditAction import AuditAction
from .AuditEntry import AuditEntry
from typing import Any
import logging
import time

__version__ = VERSION


class AuditLogger:
    """Logger for report audit trail.
    Records all actions performed on reports for compliance.
    Attributes:
        entries: Audit log entries.
    Example:
        logger=AuditLogger()
        logger.log(AuditAction.READ, "user1", "report.md")
        history=logger.get_history("report.md")
    """

    def __init__(self) -> None:
        """Initialize audit logger."""

        self.entries: list[AuditEntry] = []
        logging.debug("AuditLogger initialized")

    def log(
        self,
        action: AuditAction,
        user_id: str,
        report_id: str,
        details: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Log an action.
        Args:
            action: Action performed.
            user_id: User who performed it.
            report_id: Affected report.
            details: Additional details.
        Returns:
            Created entry.
        """

        entry = AuditEntry(
            entry_id=f"audit_{int(time.time())}_{len(self.entries)}",
            timestamp=time.time(),
            action=action,
            user_id=user_id,
            report_id=report_id,
            details=details or {},
        )
        self.entries.append(entry)
        return entry

    def get_history(self, report_id: str) -> list[AuditEntry]:
        """Get audit history for report.
        Args:
            report_id: Report ID.
        Returns:
            List of entries.
        """

        return [e for e in self.entries if e.report_id == report_id]

    def get_user_activity(self, user_id: str) -> list[AuditEntry]:
        """Get activity for user.
        Args:
            user_id: User ID.
        Returns:
            List of entries.
        """

        return [e for e in self.entries if e.user_id == user_id]
