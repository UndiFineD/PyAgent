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


"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.types import changelog_entry
from src.core.base.common.types import compliance_category
from src.core.base.common.types import compliance_result

__version__ = VERSION


class ComplianceChecker:
    """Checks changelog compliance with various requirements.

    Verifies changelog entries meet security, legal, and
    other compliance requirements.

    Example:
        >>> checker=ComplianceChecker()
        >>> results=checker.check_all(entries)
    """

    SECURITY_KEYWORDS = ["vulnerability", "cve", "security", "patch", "exploit"]
    LEGAL_KEYWORDS = ["license", "copyright", "trademark", "patent"]

    def check_security_compliance(
        self, entries: list[ChangelogEntry]
    ) -> ComplianceResult:
        """Check security compliance.

        Args:
            entries: Changelog entries to check.

        Returns:
            ComplianceResult for security category.
        """
        issues: list[str] = []
        recommendations: list[str] = []
        # Check for security entries without proper categorization
        for entry in entries:
            if any(kw in entry.description.lower() for kw in self.SECURITY_KEYWORDS):
                if entry.category != "Security":
                    issues.append(
                        f"Security-related entry not in Security category: "
                        f"{entry.description[:50]}"
                    )
                    recommendations.append(
                        "Move security-related entries to the Security section"
                    )
        return ComplianceResult(
            category=ComplianceCategory.SECURITY,
            passed=not issues,
            issues=issues,
            recommendations=recommendations,
        )

    def check_legal_compliance(self, entries: list[ChangelogEntry]) -> ComplianceResult:
        """Check legal compliance.

        Args:
            entries: Changelog entries to check.

        Returns:
            ComplianceResult for legal category.
        """
        issues: list[str] = []
        recommendations: list[str] = []
        # Check for entries that may need legal review
        for entry in entries:
            if any(kw in entry.description.lower() for kw in self.LEGAL_KEYWORDS):
                issues.append(f"Entry may need legal review: {entry.description[:50]}")
                recommendations.append(
                    "Have legal team review license / copyright changes"
                )
        return ComplianceResult(
            category=ComplianceCategory.LEGAL,
            passed=not issues,
            issues=issues,
            recommendations=recommendations,
        )

    def check_all(self, entries: list[ChangelogEntry]) -> list[ComplianceResult]:
        """Run all compliance checks.

        Args:
            entries: Changelog entries to check.

        Returns:
            List of ComplianceResult for all categories.
        """
        return [
            self.check_security_compliance(entries),
            self.check_legal_compliance(entries),
        ]
