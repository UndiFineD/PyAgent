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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Accessibility report mixin.py module.
"""

# pylint: disable=too-many-ancestors

from __future__ import annotations

from src.core.base.common.types.accessibility_report import AccessibilityReport
from src.core.base.common.types.accessibility_severity import \
    AccessibilitySeverity


class AccessibilityReportMixin:
    """Mixin for generating accessibility reports."""

    def _generate_report(self, file_path: str) -> AccessibilityReport:
        """Generate accessibility report."""
        critical_count = sum(1 for i in self.issues if i.severity == AccessibilitySeverity.CRITICAL)
        serious_count = sum(1 for i in self.issues if i.severity == AccessibilitySeverity.SERIOUS)
        # Calculate compliance score (100 - weighted issues)
        score = 100.0
        for issue in self.issues:
            if issue.severity == AccessibilitySeverity.CRITICAL:
                score -= 15
            elif issue.severity == AccessibilitySeverity.SERIOUS:
                score -= 10
            elif issue.severity == AccessibilitySeverity.MODERATE:
                score -= 5
            else:
                score -= 2
        score = max(0, score)

        # Generate recommendations
        recommendations = self._get_recommendations(critical_count, serious_count)

        return AccessibilityReport(
            file_path=file_path,
            issues=list(self.issues),
            total_elements=len(self.issues),
            wcag_level=self.target_level,
            compliance_score=round(score, 1),
            critical_count=critical_count,
            serious_count=serious_count,
            recommendations=recommendations,
        )

    def _get_recommendations(self, critical_count: int, serious_count: int) -> list[str]:
        """Helper to generate recommendations."""
        recommendations: list[str] = []
        if critical_count > 0:
            recommendations.append("Address critical accessibility issues immediately")
        if serious_count > 0:
            recommendations.append("Fix serious issues to improve basic accessibility")
        if not hasattr(self, "issues") or not self.issues:
            recommendations.append("Continue to test with screen readers and keyboard navigation")
        return recommendations
