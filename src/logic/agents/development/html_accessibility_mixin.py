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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
HTML Accessibility Mixin - Analyze HTML for accessibility issues

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
Use as a mixin on an analyzer/agent class that exposes self.issues (a list). Call _analyze_html(content: str) with HTML text to detect accessibility problems; subclass or instantiate the host class to collect AccessibilityIssue objects for each detection.

WHAT IT DOES:
Implements a lightweight HTML accessibility scanner using regular expressions to identify common issues: images missing alt attributes (MISSING_ALT_TEXT), form inputs missing associated labels (MISSING_LABEL), absent ARIA/semantic landmark regions (ARIA_MISSING), and a heading-hierarchy check entry point (_check_headings) to validate header order. For each finding it creates AccessibilityIssue instances populated with issue_type, severity, WCAG level/criterion, description, the related element snippet, line number where available, suggested_fix text, and auto_fixable flag.

WHAT IT SHOULD DO BETTER:
Replace fragile regex parsing with a proper HTML parser (BeautifulSoup, lxml, or html5lib) to correctly handle nested elements, attributes, and malformed HTML; detect labels via <label>, aria-label, aria-labelledby, and implicit labeling patterns; extend landmark detection to consider role and aria landmarks robustly; fully implement and harden heading-hierarchy checks and add unit tests, localization support, and optional safe auto-fix strategies (with preview mode) for non-destructive fixes.

FILE CONTENT SUMMARY:
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
Html accessibility mixin.py module.
"""

# pylint: disable=too-many-ancestors

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
            heading_levels.append(i
"""

# pylint: disable=too-many-ancestors

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
