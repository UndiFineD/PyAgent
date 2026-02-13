#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
Audit Logger - Report audit trail logger

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Instantiate AuditLogger and call log(action, user_id, report_id, details) to record events and use get_history(report_id) or get_user_activity(user_id) to retrieve entries; the module provides in-memory auditing of report actions via AuditEntry records with timestamps and AuditAction types. 

WHAT IT DOES:
Provides a simple in-memory audit trail: AuditLogger maintains a list of AuditEntry objects, creates entries with log(...), and filters them by report_id or user_id with get_history and get_user_activity. 

WHAT IT SHOULD DO BETTER:
Persist entries to durable storage, add concurrency/thread-safety, validate and normalize inputs, support configurable retention and export/serialization formats, and add richer querying and indexing for scale. 

FILE CONTENT SUMMARY:
Defines module metadata and imports, sets __version__ from src.core.base.lifecycle.version, and implements AuditLogger with an entries list and three primary methods: __init__, log (creates AuditEntry with id, timestamp, action, user_id, report_id, details), get_history (filter by report_id), and get_user_activity (filter by user_id).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .audit_action import AuditAction
from .audit_entry import AuditEntry

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
