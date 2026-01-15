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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.types.AccessibilityIssue import AccessibilityIssue
from src.core.base.types.AccessibilityIssueType import AccessibilityIssueType
from src.core.base.types.AccessibilityReport import AccessibilityReport
from src.core.base.types.AccessibilitySeverity import AccessibilitySeverity
from src.core.base.types.ColorContrastResult import ColorContrastResult
from src.core.base.types.WCAGLevel import WCAGLevel
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from pathlib import Path
import logging
import re

__version__ = VERSION




class AccessibilityAgent(BaseAgent):
    """Analyzer for accessibility issues in UI code.

    Detects accessibility problems and suggests improvements
    for web and GUI applications.

    Attributes:
        target_level: Target WCAG conformance level.
        issues: Detected issues.
        rules: Enabled accessibility rules.

    Example:
        analyzer=AccessibilityAgent(file_path="...", target_level=WCAGLevel.AA)
        report=analyzer.analyze_file("component.py")
        for issue in report.issues:
            print(f"{issue.severity.name}: {issue.description}")
    """

    # WCAG criterion to issue type mapping
    WCAG_CRITERIA: dict[str, tuple[AccessibilityIssueType, str]] = {
        "1.1.1": (AccessibilityIssueType.MISSING_ALT_TEXT, "Non-text Content"),
        "1.3.1": (AccessibilityIssueType.SEMANTIC_HTML, "Info and Relationships"),
        "1.4.3": (AccessibilityIssueType.LOW_COLOR_CONTRAST, "Contrast (Minimum)"),
        "1.4.6": (AccessibilityIssueType.LOW_COLOR_CONTRAST, "Contrast (Enhanced)"),
        "2.1.1": (AccessibilityIssueType.KEYBOARD_NAVIGATION, "Keyboard"),
        "2.4.3": (AccessibilityIssueType.FOCUS_MANAGEMENT, "Focus Order"),
        "2.4.6": (AccessibilityIssueType.HEADING_HIERARCHY, "Headings and Labels"),
        "3.3.1": (AccessibilityIssueType.FORM_VALIDATION, "Error Identification"),
        "3.3.2": (AccessibilityIssueType.MISSING_LABEL, "Labels or Instructions"),
        "4.1.2": (AccessibilityIssueType.ARIA_MISSING, "Name, Role, Value"),
    }

    def __init__(self, target_level: WCAGLevel | str = WCAGLevel.AA, file_path: str | None = None) -> None:
        """Initialize accessibility analyzer.

        Args:
            target_level: Target WCAG conformance level.
            file_path: Path to the agent file.
        """
        super().__init__(file_path if file_path else "virtual_accessibility_agent")

        # Robust handling of target_level
        if isinstance(target_level, str):
            try:
                # remove 'WCAGLevel.' prefix if present
                clean_level = target_level.split('.')[-1]
                self.target_level = WCAGLevel[clean_level]
            except KeyError:
                self.target_level = WCAGLevel.AA
        else:
            self.target_level = target_level

        self.issues: list[AccessibilityIssue] = []
        self.rules: dict[str, bool] = {rule: True for rule in self.WCAG_CRITERIA}
        logging.debug(f"AccessibilityAgent initialized with level {self.target_level.value}")

    @as_tool
    def analyze_file(self, file_path: str) -> AccessibilityReport:
        """Analyze a file for accessibility issues.

        Args:
            file_path: Path to file to analyze.

        Returns:
            Comprehensive accessibility report.
        """
        self.issues.clear()
        path = Path(file_path)
        if not path.exists():
            return AccessibilityReport(file_path=file_path)
        content = path.read_text(encoding="utf-8")
        # Analyze based on file type
        if path.suffix in (".html", ".htm"):
            self._analyze_html(content)
        elif path.suffix == ".py":
            self._analyze_python_ui(content)
        elif path.suffix in (".js", ".jsx", ".ts", ".tsx"):
            self._analyze_javascript_ui(content)
        return self._generate_report(file_path)

    def analyze_content(self, content: str, file_type: str = "html") -> AccessibilityReport:
        """Analyze content string for accessibility issues.

        Args:
            content: Content to analyze.
            file_type: Type of content (html, python, javascript).

        Returns:
            Accessibility report.
        """
        self.issues.clear()
        if file_type == "html":
            self._analyze_html(content)
        elif file_type == "python":
            self._analyze_python_ui(content)
        elif file_type in ("javascript", "react"):
            self._analyze_javascript_ui(content)
        return self._generate_report("content")

    def _analyze_html(self, content: str) -> None:
        """Analyze HTML content for accessibility issues.

        Args:
            content: HTML content string.
        """
        # Check for images without alt text
        img_pattern = r'<img\s+[^>]*?(?<!alt=)[^>]*?>'
        for match in re.finditer(img_pattern, content, re.IGNORECASE):
            if 'alt=' not in match.group().lower():
                line_num = content[:match.start()].count('\n') + 1
                issue: AccessibilityIssue = AccessibilityIssue(
                    issue_type=AccessibilityIssueType.MISSING_ALT_TEXT,
                    severity=AccessibilitySeverity.CRITICAL,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="1.1.1",
                    description="Image missing alt attribute",
                    element=match.group()[:50],
                    line_number=line_num,
                    suggested_fix=(
                        'Add alt="" for decorative or alt="description" '
                        'for meaningful images'
                    ),
                    auto_fixable=False)
                self.issues.append(issue)
        # Check for form inputs without labels
        input_pattern = r'<input\s+[^>]*?>'
        for match in re.finditer(input_pattern, content, re.IGNORECASE):
            input_tag = match.group()
            if 'type="hidden"' not in input_tag.lower():
                # Check if there's a label for this input
                input_id_match = re.search(r'id=["\']([^"\']+)["\']', input_tag)
                if input_id_match:
                    input_id = input_id_match.group(1)
                    if f'for="{input_id}"' not in content and f"for='{input_id}'" not in content:
                        line_num = content[:match.start()].count('\n') + 1
                        self.issues.append(AccessibilityIssue(
                            issue_type=AccessibilityIssueType.MISSING_LABEL,
                            severity=AccessibilitySeverity.SERIOUS,
                            wcag_level=WCAGLevel.A,
                            wcag_criterion="3.3.2",
                            description="Form input missing associated label",
                            element=input_tag[:50],
                            line_number=line_num,
                            suggested_fix=f'Add <label for="{input_id}">Label text</label>',
                            auto_fixable=False
                        ))
        # Check for missing ARIA landmarks
        landmarks = ['main', 'nav', 'header', 'footer', 'aside']
        has_landmark = any(
            f'<{tag}' in content.lower() or f'role="{tag}"' in content.lower()
            for tag in landmarks
        )
        if not has_landmark and '<body' in content.lower():
            self.issues.append(
                AccessibilityIssue(
                    issue_type=AccessibilityIssueType.ARIA_MISSING,
                    severity=AccessibilitySeverity.MODERATE,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="4.1.2",
                    description="Page missing landmark regions",
                    element="document",
                    suggested_fix=(
                        "Add semantic HTML5 elements (main, nav, header, "
                        "footer) or ARIA landmarks"
                    ),
                    auto_fixable=False
                )
            )
        # Check heading hierarchy
        heading_levels: list[int] = []
        for match in re.finditer(r'<h([1-6])', content, re.IGNORECASE):
            heading_levels.append(int(match.group(1)))
        if heading_levels:
            if heading_levels[0] != 1:
                self.issues.append(AccessibilityIssue(
                    issue_type=AccessibilityIssueType.HEADING_HIERARCHY,
                    severity=AccessibilitySeverity.MODERATE,
                    wcag_level=WCAGLevel.AA,
                    wcag_criterion="2.4.6",
                    description="Page should start with an h1 heading",
                    element="headings",
                    suggested_fix="Start page with <h1> element",
                    auto_fixable=False
                ))
            # Check for skipped levels
            for i in range(1, len(heading_levels)):
                if heading_levels[i] > heading_levels[i - 1] + 1:
                    self.issues.append(AccessibilityIssue(
                        issue_type=AccessibilityIssueType.HEADING_HIERARCHY,
                        severity=AccessibilitySeverity.MODERATE,
                        wcag_level=WCAGLevel.AA,
                        wcag_criterion="2.4.6",
                        description=(
                            f"Heading level skipped: "
                            f"h{heading_levels[i - 1]} to h{heading_levels[i]}"
                        ),
                        element=f"h{heading_levels[i]}",
                        suggested_fix="Use sequential heading levels without skipping",
                        auto_fixable=False
                    ))

    def _analyze_python_ui(self, content: str) -> None:
        """Analyze Python UI code (tkinter, PyQt, etc.) for accessibility issues.

        Args:
            content: Python source code.
        """
        # Check for tkinter widgets without accessibility properties
        widget_patterns = [
            (r'Button\s*\([^)]*\)', "Button"),
            (r'Label\s*\([^)]*\)', "Label"),
            (r'Entry\s*\([^)]*\)', "Entry"),
            (r'Canvas\s*\([^)]*\)', "Canvas"),
        ]
        for pattern, widget_name in widget_patterns:
            for match in re.finditer(pattern, content):
                widget_call = match.group()
                line_num = content[:match.start()].count('\n') + 1
                # Check for keyboard bindings
                if 'bind' not in content[match.end():match.end() + 200]:
                    # Check if there's a bind call near this widget
                    pass  # More complex analysis would be needed
                # Check for tooltips / accessibility text
                if 'tooltip' not in widget_call.lower() and 'help' not in widget_call.lower():
                    self.issues.append(AccessibilityIssue(
                        issue_type=AccessibilityIssueType.ARIA_MISSING,
                        severity=AccessibilitySeverity.MINOR,
                        wcag_level=WCAGLevel.AA,
                        wcag_criterion="4.1.2",
                        description=f"{widget_name} widget may benefit from tooltip or help text",
                        element=widget_call[:50],
                        line_number=line_num,
                        suggested_fix="Consider adding tooltip or accessibility description",
                        auto_fixable=False
                    ))

    def _analyze_javascript_ui(self, content: str) -> None:
        """Analyze JavaScript / React UI code for accessibility issues.

        Args:
            content: JavaScript / React source code.
        """
        # Check for click handlers without keyboard support
        click_pattern = r'onClick\s*=\s*\{[^}]+\}'
        for match in re.finditer(click_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            # Check if there's also onKeyPress / onKeyDown nearby
            context = content[max(0, match.start() - 100):match.end() + 100]
            if 'onKeyPress' not in context and 'onKeyDown' not in context:
                self.issues.append(AccessibilityIssue(
                    issue_type=AccessibilityIssueType.KEYBOARD_NAVIGATION,
                    severity=AccessibilitySeverity.SERIOUS,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="2.1.1",
                    description="Click handler without keyboard equivalent",
                    element=match.group()[:50],
                    line_number=line_num,
                    suggested_fix="Add onKeyPress or onKeyDown handler for keyboard users",
                    auto_fixable=False
                ))

        # Check for div / span used as interactive elements
        interactive_div = r'<div\b[^>]*\bonClick\s*=\s*\{[^}]+\}[^>]*>'
        for match in re.finditer(interactive_div, content, re.IGNORECASE):
            line_num = content[:match.start()].count('\n') + 1
            context = match.group()
            context_lower = context.lower()
            if 'role=' not in context_lower and 'tabindex' not in context_lower:
                self.issues.append(AccessibilityIssue(
                    issue_type=AccessibilityIssueType.SEMANTIC_HTML,
                    severity=AccessibilitySeverity.SERIOUS,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="1.3.1",
                    description="Interactive div should be a button or have role / tabIndex",
                    element=context[:50],
                    line_number=line_num,
                    suggested_fix='Use <button> or add role="button" tabIndex="0"',
                    auto_fixable=False
                ))

    def check_color_contrast(
        self,
        foreground: str,
        background: str,
        is_large_text: bool = False
    ) -> ColorContrastResult:
        """Check color contrast ratio.

        Args:
            foreground: Foreground color (hex).
            background: Background color (hex).
            is_large_text: Whether text is large (14pt bold or 18pt+).

        Returns:
            Color contrast analysis result.
        """
        fg_luminance = self._relative_luminance(foreground)
        bg_luminance = self._relative_luminance(background)

        lighter = max(fg_luminance, bg_luminance)
        darker = min(fg_luminance, bg_luminance)
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)

        # WCAG AA: 4.5:1 for normal text, 3:1 for large text
        # WCAG AAA: 7:1 for normal text, 4.5:1 for large text
        min_aa = 3.0 if is_large_text else 4.5
        min_aaa = 4.5 if is_large_text else 7.0

        return ColorContrastResult(
            foreground=foreground,
            background=background,
            contrast_ratio=round(contrast_ratio, 2),
            passes_aa=contrast_ratio >= min_aa,
            passes_aaa=contrast_ratio >= min_aaa,
            min_ratio_aa=min_aa,
            min_ratio_aaa=min_aaa
        )

    def _relative_luminance(self, hex_color: str) -> float:
        """Calculate relative luminance of a color.

        Args:
            hex_color: Hex color string (e.g., "#FFFFFF").

        Returns:
            Relative luminance value.
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c * 2 for c in hex_color])

        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255

        def adjust(c: float) -> float:
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    def _generate_report(self, file_path: str) -> AccessibilityReport:
        """Generate accessibility report.

        Args:
            file_path: Path to analyzed file.

        Returns:
            Comprehensive accessibility report.
        """
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
        recommendations: list[str] = []
        if critical_count > 0:
            recommendations.append("Address critical accessibility issues immediately")
        if serious_count > 0:
            recommendations.append("Fix serious issues to improve basic accessibility")
        if not self.issues:
            recommendations.append("Continue to test with screen readers and keyboard navigation")
        return AccessibilityReport(
            file_path=file_path,
            issues=list(self.issues),
            total_elements=len(self.issues),
            wcag_level=self.target_level,
            compliance_score=round(score, 1),
            critical_count=critical_count,
            serious_count=serious_count,
            recommendations=recommendations
        )

    def get_issues_by_severity(
        self,
        severity: AccessibilitySeverity
    ) -> list[AccessibilityIssue]:
        """Get issues filtered by severity.

        Args:
            severity: Severity level to filter by.

        Returns:
            List of issues with specified severity.
        """
        return [i for i in self.issues if i.severity == severity]

    def get_issues_by_wcag_level(
        self,
        level: WCAGLevel
    ) -> list[AccessibilityIssue]:
        """Get issues filtered by WCAG level.

        Args:
            level: WCAG level to filter by.

        Returns:
            List of issues affecting specified level.
        """
        return [i for i in self.issues if i.wcag_level == level]

    def enable_rule(self, wcag_criterion: str) -> None:
        """Enable a specific WCAG rule.

        Args:
            wcag_criterion: WCAG criterion identifier.
        """
        if wcag_criterion in self.rules:
            self.rules[wcag_criterion] = True

    def disable_rule(self, wcag_criterion: str) -> None:
        """Disable a specific WCAG rule.

        Args:
            wcag_criterion: WCAG criterion identifier.
        """
        if wcag_criterion in self.rules:
            self.rules[wcag_criterion] = False
