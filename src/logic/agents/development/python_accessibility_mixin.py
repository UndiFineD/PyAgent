#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

from __future__ import annotations
import re
from src.core.base.common.types.accessibility_issue import AccessibilityIssue
from src.core.base.common.types.accessibility_issue_type import AccessibilityIssueType
from src.core.base.common.types.accessibility_severity import AccessibilitySeverity
from src.core.base.common.types.wcag_level import WCAGLevel

class PythonAccessibilityMixin:
    """Mixin for Python UI accessibility analysis."""

    def _analyze_python_ui(self, content: str) -> None:
        """Analyze Python UI code (tkinter, PyQt, etc.) for accessibility issues."""
        # Check for tkinter widgets without accessibility properties
        widget_patterns = [
            (r"Button\s*\([^)]*\)", "Button"),
            (r"Label\s*\([^)]*\)", "Label"),
            (r"Entry\s*\([^)]*\)", "Entry"),
            (r"Canvas\s*\([^)]*\)", "Canvas"),
        ]
        for pattern, widget_name in widget_patterns:
            for match in re.finditer(pattern, content):
                widget_call = match.group()
                line_num = content[: match.start()].count("\n") + 1

                # Check for tooltips / accessibility text
                if (
                    "tooltip" not in widget_call.lower()
                    and "help" not in widget_call.lower()
                ):
                    self.issues.append(
                        AccessibilityIssue(
                            issue_type=AccessibilityIssueType.ARIA_MISSING,
                            severity=AccessibilitySeverity.MINOR,
                            wcag_level=WCAGLevel.AA,
                            wcag_criterion="4.1.2",
                            description=f"{widget_name} widget may benefit from tooltip or help text",
                            element=widget_call[:50],
                            line_number=line_num,
                            suggested_fix="Consider adding tooltip or accessibility description",
                            auto_fixable=False,
                        )
                    )
