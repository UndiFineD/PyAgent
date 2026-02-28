#!/usr/bin/env python3

"""
Javascript accessibility mixin.py module.
"""

# pylint: disable=too-many-ancestors
# Copyright 2026 PyAgent Authors

from __future__ import annotations

import re

from src.core.base.common.types.accessibility_issue import AccessibilityIssue
from src.core.base.common.types.accessibility_issue_type import \
    AccessibilityIssueType
from src.core.base.common.types.accessibility_severity import \
    AccessibilitySeverity
from src.core.base.common.types.wcag_level import WCAGLevel


class JavascriptAccessibilityMixin:
    """Mixin for Javascript UI accessibility analysis."""

    def _analyze_javascript_ui(self, content: str) -> None:
        """Analyze JavaScript / React UI code for accessibility issues."""
        # Check for click handlers without keyboard support
        click_pattern = r"onClick\s*=\s*\{[^}]+\}"
        for match in re.finditer(click_pattern, content):
            line_num = content[: match.start()].count("\n") + 1
            # Check if there's also onKeyPress / onKeyDown nearby
            context = content[max(0, match.start() - 100) : match.end() + 100]
            if "onKeyPress" not in context and "onKeyDown" not in context:
                self.issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.KEYBOARD_NAVIGATION,
                        severity=AccessibilitySeverity.SERIOUS,
                        wcag_level=WCAGLevel.A,
                        wcag_criterion="2.1.1",
                        description="Click handler without keyboard equivalent",
                        element=match.group()[:50],
                        line_number=line_num,
                        suggested_fix="Add onKeyPress or onKeyDown handler for keyboard users",
                        auto_fixable=False,
                    )
                )

        # Check for div / span used as interactive elements
        interactive_div = r"<div\b[^>]*\bonClick\s*=\s*\{[^}]+\}[^>]*>"
        for match in re.finditer(interactive_div, content, re.IGNORECASE):
            line_num = content[: match.start()].count("\n") + 1
            context = match.group()
            context_lower = context.lower()
            if "role=" not in context_lower and "tabindex" not in context_lower:
                self.issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.SEMANTIC_HTML,
                        severity=AccessibilitySeverity.SERIOUS,
                        wcag_level=WCAGLevel.A,
                        wcag_criterion="1.3.1",
                        description="Interactive div should be a button or have role / tabIndex",
                        element=context[:50],
                        line_number=line_num,
                        suggested_fix='Use <button> or add role="button" tabIndex="0"',
                        auto_fixable=False,
                    )
                )
