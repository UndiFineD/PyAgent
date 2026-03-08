#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/AccessibilityReportMixin.description.md

# AccessibilityReportMixin

**File**: `src\logic\agents\development\AccessibilityReportMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 57  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for AccessibilityReportMixin.

## Classes (1)

### `AccessibilityReportMixin`

Mixin for generating accessibility reports.

**Methods** (2):
- `_generate_report(self, file_path)`
- `_get_recommendations(self, critical_count, serious_count)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `src.core.base.types.AccessibilityReport.AccessibilityReport`
- `src.core.base.types.AccessibilitySeverity.AccessibilitySeverity`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/AccessibilityReportMixin.improvements.md

# Improvements for AccessibilityReportMixin

**File**: `src\logic\agents\development\AccessibilityReportMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 57 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AccessibilityReportMixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors

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

    def _get_recommendations(
        self, critical_count: int, serious_count: int
    ) -> list[str]:
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
