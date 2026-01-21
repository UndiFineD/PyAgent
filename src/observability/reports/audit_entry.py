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
from src.core.base.version import VERSION
from .audit_action import AuditAction
from dataclasses import dataclass, field
from typing import Any

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
