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
AuditEntry - AuditEntry dataclass for audit logs

[Brief Summary]
A small dataclass representing a single audit log entry used by agent report generation and audit trails. It captures identity, timing, action, affected report, and arbitrary details in a typed container for downstream serialization or processing.
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Instantiate and populate for recording or serializing audit events, e.g.:
from src.core.models.audit_entry import AuditEntry
entry = AuditEntry(entry_id="e123", timestamp=1670000000.0, action=AuditAction.CREATED, user_id="alice", report_id="r456", details={"notes": "initial import"})

WHAT IT DOES:
- Defines a compact, typed container for audit information used across reporting and lifecycle modules.
- Provides default-free fields for required metadata and a default empty dict for flexible details.
- Exposes a stable __version__ sourced from the project's VERSION constant to track compatibility.

WHAT IT SHOULD DO BETTER:
- Add explicit validation (types, UUID format for entry_id, non-negative timestamp) and factory methods (from_dict, to_dict) to ease serialization and deserialization.
- Use timezone-aware timestamps (datetime[tz]) or provide helpers to convert epoch floats to aware datetimes.
- Harden the details field with a TypedDict or schema to document expected keys, and consider redaction helpers for sensitive fields before logging/serialization.
- Provide __post_init__ for normalization (e.g., coerce AuditAction from str) and unit tests demonstrating typical serialization and validation behavior.

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
"""

from __future__ import annotations

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
