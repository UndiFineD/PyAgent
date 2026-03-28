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

"""Deterministic scan report model for secret scanning decisions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

_ALLOWED_STATUSES = {"PASS", "FAIL", "ERROR"}
_BLOCKING_SEVERITIES = {"HIGH", "CRITICAL"}


@dataclass(frozen=True, slots=True)
class ScanReport:
    """Represents a single scan execution result.

    Attributes:
        run_id: Stable identifier for one scanner execution.
        status: Canonical scan status: PASS, FAIL, or ERROR.
        findings: Raw finding dictionaries from scanner output.
        blocking: Whether this report should block pipeline progression.
        error_message: Optional error details when scanner execution fails.

    """

    run_id: str
    status: str
    findings: list[dict[str, Any]] = field(default_factory=list)
    blocking: bool | None = None
    error_message: str = ""

    def __post_init__(self) -> None:
        """Validate scan report fields and derive blocking decision.

        Raises:
            ValueError: If required report fields are invalid.

        """
        if not self.run_id:
            msg = "run_id is required"
            raise ValueError(msg)
        if self.status not in _ALLOWED_STATUSES:
            msg = f"status must be one of {_ALLOWED_STATUSES}"
            raise ValueError(msg)

        if self.blocking is None:
            has_high_findings = any(
                str(item.get("severity", "")).upper() in _BLOCKING_SEVERITIES
                for item in self.findings
            )
            derived_blocking = self.status == "ERROR" or has_high_findings
            object.__setattr__(self, "blocking", derived_blocking)
