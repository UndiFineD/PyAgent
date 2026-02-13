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
Compliance core.py module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ComplianceIssue:
    """Represents a regulatory or policy violation found in code."""

    severity: str
    category: str
    message: str
    file_path: str


class ComplianceCore:
    """Pure logic for continuous compliance auditing and regulatory scanning.
    Identifies licensing conflicts, PII leaks, and dependency risks.
    """

    FORBIDDEN_KEYWORDS = [
        r"password\s*=\s*['\"].+['\"]",
        r"api_key\s*=\s*['\"].+['\"]",
        r"aws_secret",
        r"BEGIN RSA PRIVATE KEY",
    ]

    ALLOWED_LICENSES = ["MIT", "Apache-2.0", "BSD-3-Clause", "PSF-2.0"]

    def audit_content(self, content: str, file_path: str) -> list[ComplianceIssue]:
        """Scans content for common compliance and security violations."""
        try:
            from rust_core import \
                audit_content_rust  # type: ignore[attr-defined]

            raw_issues = audit_content_rust(content, file_path)
            return [ComplianceIssue(severity=s, category=c, message=m, file_path=f) for s, c, m, f in raw_issues]
        except (ImportError, AttributeError):
            issues = []

            # 1. Secret Scanning
            for pattern in self.FORBIDDEN_KEYWORDS:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(
                        ComplianceIssue(
                            severity="CRITICAL",
                            category="Secret Leak",
                            message=f"Potential credential found matching pattern: {pattern}",
                            file_path=file_path,
                        )
                    )

            # 2. License Detection (Basic)
            if "LICENSE" in file_path.upper():
                found_license = False
                for lic in self.ALLOWED_LICENSES:
                    if lic in content:
                        found_license = True
                        break
                if not found_license:
                    issues.append(
                        ComplianceIssue(
                            severity="WARNING",
                            category="Licensing",
                            message="Unrecognized or non-standard license detected.",
                            file_path=file_path,
                        )
                    )

            return issues

    def aggregate_score(self, issues: list[ComplianceIssue]) -> float:
        """Calculates a compliance score from 0.0 to 1.0."""
        try:
            from rust_core import \
                aggregate_score_rust  # type: ignore[attr-defined]

            return aggregate_score_rust([issue.severity for issue in issues])
        except (ImportError, AttributeError):
            if not issues:
                return 1.0

            deductions = {"CRITICAL": 0.5, "WARNING": 0.1, "INFO": 0.02}

        score = 1.0
        for issue in issues:
            score -= deductions.get(issue.severity, 0.0)

        return max(0.0, score)
