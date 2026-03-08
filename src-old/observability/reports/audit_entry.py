#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/reports/audit_entry.description.md

# Description: src/observability/reports/audit_entry.py

Module overview:
- Defines `AuditEntry` dataclass for representing audit log records related to report actions.

Behavioral notes:
- Dependencies: `AuditAction` enum/class from the same package.
- Simple data container used by audit logging systems.
## Source: src-old/observability/reports/audit_entry.improvements.md

# Improvements: src/observability/reports/audit_entry.py

Suggested improvements (automatically generated):
- Add unit tests covering core behavior and edge cases.
- Break large modules into smaller, testable components.
- Avoid heavy imports at module import time; import lazily where appropriate.
- Add type hints and explicit return types for public functions.
- Add logging and better error handling for file and IO operations.
- Consider dependency injection for filesystem and environment interactions.

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


"""Auto-extracted class from generate_agent_reports.py"""


from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .audit_action import AuditAction

__version__ = VERSION


@dataclass
class AuditEntry:
    """Audit log entry.
    Attributes:
        entry_id: Unique entry identifier.
        timestamp: Event timestamp.
        action: Audit action.
        user_id: User who performed action.
        report_id: Affected report.
        details: Additional details.
    """

    entry_id: str
    timestamp: float
    action: AuditAction
    user_id: str
    report_id: str
    details: dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
