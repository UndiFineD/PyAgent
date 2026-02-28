#!/usr/bin/env python3

"""
Html accessibility mixin.py module.
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


class HtmlAccessibilityMixin:
    """Mixin for HTML accessibility analysis."""

    def _analyze_html(self, content: str) -> None:
        """Analyze HTML content for accessibility issues."""
        # Check for images without alt text
        img_pattern = r"<img\s+[^>]*?(?<!alt=)[^>]*?>"
        for match in re.finditer(img_pattern, content, re.IGNORECASE):
            if "alt=" not in match.group().lower():
                line_num = content[: match.start()].count("\n") + 1
                issue: AccessibilityIssue = AccessibilityIssue(
                    issue_type=AccessibilityIssueType.MISSING_ALT_TEXT,
                    severity=AccessibilitySeverity.CRITICAL,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="1.1.1",
                    description="Image missing alt attribute",
                    element=match.group()[:50],
                    line_number=line_num,
                    suggested_fix=('Add alt="" for decorative or alt="description" for meaningful images'),
                    auto_fixable=False,
                )
                self.issues.append(issue)

        # Check for form inputs without labels
        input_pattern = r"<input\s+[^>]*?>"
        for match in re.finditer(input_pattern, content, re.IGNORECASE):
            input_tag = match.group()
            if 'type="hidden"' not in input_tag.lower():
                # Check if there's a label for this input
                input_id_match = re.search(r'id=["\']([^"\']+)["\']', input_tag)
                if input_id_match:
                    input_id = input_id_match.group(1)
                    if f'for="{input_id}"' not in content and f"for='{input_id}'" not in content:
                        line_num = content[: match.start()].count("\n") + 1
                        self.issues.append(
                            AccessibilityIssue(
                                issue_type=AccessibilityIssueType.MISSING_LABEL,
                                severity=AccessibilitySeverity.SERIOUS,
                                wcag_level=WCAGLevel.A,
                                wcag_criterion="3.3.2",
                                description="Form input missing associated label",
                                element=input_tag[:50],
                                line_number=line_num,
                                suggested_fix=f'Add <label for="{input_id}">Label text</label>',
                                auto_fixable=False,
                            )
                        )

        # Check for missing ARIA landmarks
        landmarks = ["main", "nav", "header", "footer", "aside"]
        has_landmark = any(f"<{tag}" in content.lower() or f'role="{tag}"' in content.lower() for tag in landmarks)
        if not has_landmark and "<body" in content.lower():
            self.issues.append(
                AccessibilityIssue(
                    issue_type=AccessibilityIssueType.ARIA_MISSING,
                    severity=AccessibilitySeverity.MODERATE,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="4.1.2",
                    description="Page missing landmark regions",
                    element="document",
                    suggested_fix=("Add semantic HTML5 elements (main, nav, header, footer) or ARIA landmarks"),
                    auto_fixable=False,
                )
            )

        # Check heading hierarchy
        self._check_headings(content)

    def _check_headings(self, content: str) -> None:
        """Helper to check heading hierarchy."""
        heading_levels: list[int] = []
        for match in re.finditer(r"<h([1-6])", content, re.IGNORECASE):
            heading_levels.append(int(match.group(1)))

        if heading_levels:
            if heading_levels[0] != 1:
                self.issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.HEADING_HIERARCHY,
                        severity=AccessibilitySeverity.MODERATE,
                        wcag_level=WCAGLevel.AA,
                        wcag_criterion="2.4.6",
                        description="Page should start with an h1 heading",
                        element="headings",
                        suggested_fix="Start page with <h1> element",
                        auto_fixable=False,
                    )
                )
            # Check for skipped levels
            for i in range(1, len(heading_levels)):
                if heading_levels[i] > heading_levels[i - 1] + 1:
                    self.issues.append(
                        AccessibilityIssue(
                            issue_type=AccessibilityIssueType.HEADING_HIERARCHY,
                            severity=AccessibilitySeverity.MODERATE,
                            wcag_level=WCAGLevel.AA,
                            wcag_criterion="2.4.6",
                            description=(f"Heading level skipped: h{heading_levels[i - 1]} to h{heading_levels[i]}"),
                            element=f"h{heading_levels[i]}",
                            suggested_fix="Use sequential heading levels without skipping",
                            auto_fixable=False,
                        )
                    )
