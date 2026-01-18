#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

from __future__ import annotations
from src.core.base.types.AccessibilityReport import AccessibilityReport
from src.core.base.types.AccessibilitySeverity import AccessibilitySeverity

class AccessibilityReportMixin:
    """Mixin for generating accessibility reports."""

    def _generate_report(self, file_path: str) -> AccessibilityReport:
        """Generate accessibility report."""
        critical_count = sum(
            1 for i in self.issues if i.severity == AccessibilitySeverity.CRITICAL
        )
        serious_count = sum(
            1 for i in self.issues if i.severity == AccessibilitySeverity.SERIOUS
        )
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
            recommendations.append(
                "Continue to test with screen readers and keyboard navigation"
            )
        return recommendations
