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

"""Reporting and recording logic for SecurityCore."""

from __future__ import annotations

import logging
import time

from src.core.base.common.types.security_vulnerability import SecurityVulnerability


class SecurityReporterMixin:
    """Mixin for security reporting and recording findings."""

    def _record_finding(self, issue_type: str, severity: str, desc: str) -> None:
        """Records security findings for fleet intelligence (Phase 108)."""
        if hasattr(self, "recorder") and self.recorder:
            try:
                self.recorder.record_lesson(
                    "security_vulnerability",
                    {
                        "type": issue_type,
                        "severity": severity,
                        "description": desc,
                        "timestamp": time.time(),
                    },
                )
            except (AttributeError, RuntimeError, TypeError) as e:
                logging.debug(f"SecurityCore: Failed to record finding: {e}")

    def get_risk_level(self, vulnerabilities: list[SecurityVulnerability]) -> str:
        """Determines the overall risk level for a report."""
        severities = [v.severity for v in vulnerabilities]
        if "critical" in severities or "CRITICAL" in [s.upper() for s in severities]:
            return "CRITICAL"
        if "high" in severities or "HIGH" in [s.upper() for s in severities]:
            return "HIGH"
        if "medium" in severities or "MEDIUM" in [s.upper() for s in severities]:
            return "MEDIUM"
        return "LOW"
