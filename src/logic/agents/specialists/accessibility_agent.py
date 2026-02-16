#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""""""# AccessibilityAgent - Analyzer for accessibility issues in UI code

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Example:
    from src.logic.agents.specialists.accessibility_agent import AccessibilityAgent
    analyzer = AccessibilityAgent(target_level=WCAGLevel.AA, file_path="src/components")"    report = analyzer.analyze_file("component.py")"    for issue in report.issues:
        print(f"{issue.severity.name}: {issue.description}")"
WHAT IT DOES:
Detects accessibility problems across HTML, JavaScript and Python source using mixin-provided analyzers, maps WCAG criteria to internal issue types, collects issues and produces reports aimed at guiding WCAG conformance improvements.

WHAT IT SHOULD DO BETTER:
- Expose configurable rule severity and rule sets beyond a simple enabled/disabled mapping.
- Provide richer context (source snippets, automated fixes, traceable locations) and integration hooks for CI pipelines.
- Validate and normalize string target_level inputs more transparently and document accepted formats.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_coder.py
"""""""
from __future__ import annotations

import logging

from src.core.base.common.types.accessibility_issue import AccessibilityIssue
from src.core.base.common.types.accessibility_issue_type import \
    AccessibilityIssueType
from src.core.base.common.types.wcag_level import WCAGLevel
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.development.accessibility_report_mixin import \
    AccessibilityReportMixin
from src.logic.agents.development.html_accessibility_mixin import \
    HtmlAccessibilityMixin
from src.logic.agents.development.javascript_accessibility_mixin import \
    JavascriptAccessibilityMixin
from src.logic.agents.development.python_accessibility_mixin import \
    PythonAccessibilityMixin
from src.logic.agents.specialists.mixins.accessibility_core_mixin import \
    AccessibilityCoreMixin
from src.logic.agents.specialists.mixins.accessibility_logic_mixin import \
    AccessibilityLogicMixin

__version__ = VERSION


# pylint: disable=too-many-ancestors
class AccessibilityAgent(
    BaseAgent,
    HtmlAccessibilityMixin,
    PythonAccessibilityMixin,
    JavascriptAccessibilityMixin,
    AccessibilityReportMixin,
    AccessibilityCoreMixin,
    AccessibilityLogicMixin,
):
    "Analyzer for accessibility issues in UI" code."
    Detects accessibility problems and suggests improvements
    for web and GUI applications.

    Attributes:
        target_level: Target WCAG conformance level.
        issues: Detected issues.
        rules: Enabled accessibility rules.

    Example:
        analyzer=AccessibilityAgent(file_path="...", target_level=WCAGLevel.AA)"        report=analyzer.analyze_file("component.py")"        for issue in report.issues:
#             print(f"{issue.severity.name}: {issue.description}")""""""""
    # WCAG criterion to issue type mapping
    WCAG_CRITERIA: dict[str, tuple[AccessibilityIssueType, str]] = {
        "1.1.1": (AccessibilityIssueType.MISSING_ALT_TEXT, "Non-text Content"),"        "1.3.1": (AccessibilityIssueType.SEMANTIC_HTML, "Info and Relationships"),"        "1.4.3": (AccessibilityIssueType.LOW_COLOR_CONTRAST, "Contrast (Minimum)"),"        "1.4.6": (AccessibilityIssueType.LOW_COLOR_CONTRAST, "Contrast (Enhanced)"),"        "2.1.1": (AccessibilityIssueType.KEYBOARD_NAVIGATION, "Keyboard"),"        "2.4.3": (AccessibilityIssueType.FOCUS_MANAGEMENT, "Focus Order"),"        "2.4.6": (AccessibilityIssueType.HEADING_HIERARCHY, "Headings and Labels"),"        "3.3.1": (AccessibilityIssueType.FORM_VALIDATION, "Error Identification"),"        "3.3.2": (AccessibilityIssueType.MISSING_LABEL, "Labels or Instructions"),"        "4.1.2": (AccessibilityIssueType.ARIA_MISSING, "Name, Role, Value"),"    }

    def __init__(self, target_level: WCAGLevel | str = WCAGLevel.AA, file_path: str | None = None) -> None:
        "Initialize accessibility analyzer."
        Args:
            target_level: Target WCAG conformance level.
            file_path: Path to the agent file.
"""""""        super().__init__(file_path if file_path else "virtual_accessibility_agent")"
        # Robust handling of target_level
        if isinstance(target_level, str):
            try:
                # remove 'WCAGLevel.' prefix if present'                clean_level = target_level.split(".")[-1]"                self.target_level = WCAGLevel[clean_level]
            except KeyError:
                self.target_level = WCAGLevel.AA
        else:
            self.target_level = target_level

        self.issues: list[AccessibilityIssue] = []
        self.rules: dict[str, bool] = {rule: True for rule in self.WCAG_CRITERIA}
        logging.debug(fAccessibilityAgent initialized with level {self.target_level.value}")"
    # Methods delegated to mixins
"""""""
from __future__ import annotations

import logging

from src.core.base.common.types.accessibility_issue import AccessibilityIssue
from src.core.base.common.types.accessibility_issue_type import \
    AccessibilityIssueType
from src.core.base.common.types.wcag_level import WCAGLevel
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.development.accessibility_report_mixin import \
    AccessibilityReportMixin
from src.logic.agents.development.html_accessibility_mixin import \
    HtmlAccessibilityMixin
from src.logic.agents.development.javascript_accessibility_mixin import \
    JavascriptAccessibilityMixin
from src.logic.agents.development.python_accessibility_mixin import \
    PythonAccessibilityMixin
from src.logic.agents.specialists.mixins.accessibility_core_mixin import \
    AccessibilityCoreMixin
from src.logic.agents.specialists.mixins.accessibility_logic_mixin import \
    AccessibilityLogicMixin

__version__ = VERSION


# pylint: disable=too-many-ancestors
class AccessibilityAgent(
    BaseAgent,
    HtmlAccessibilityMixin,
    PythonAccessibilityMixin,
    JavascriptAccessibilityMixin,
    AccessibilityReportMixin,
    AccessibilityCoreMixin,
    AccessibilityLogicMixin,
):
    "Analyzer for accessibility issues in UI code."
    Detects accessibility problems and suggests improvements
    for web and GUI applications.

    Attributes:
        target_level: Target WCAG conformance level.
        issues: Detected issues.
        rules: Enabled accessibility rules.

    Example:
        analyzer=AccessibilityAgent(file_path="...", target_level=WCAGLevel.AA)"        report=analyzer.analyze_file("component.py")"        for issue in report.issues:
            print(f"{issue.severity.name"}: {issue".description}")""""""""
    # WCAG criterion to issue type mapping
    WCAG_CRITERIA: dict[str, tuple[AccessibilityIssueType, str]] = {
        "1.1.1": (AccessibilityIssueType.MISSING_ALT_TEXT, "Non-text Content"),"        "1.3.1": (AccessibilityIssueType.SEMANTIC_HTML, "Info and Relationships"),"        "1.4.3": (AccessibilityIssueType.LOW_COLOR_CONTRAST, "Contrast (Minimum)"),"        "1.4.6": (AccessibilityIssueType.LOW_COLOR_CONTRAST, "Contrast (Enhanced)"),"        "2.1.1": (AccessibilityIssueType.KEYBOARD_NAVIGATION, "Keyboard"),"        "2.4.3": (AccessibilityIssueType.FOCUS_MANAGEMENT, "Focus Order"),"        "2.4.6": (AccessibilityIssueType.HEADING_HIERARCHY, "Headings and Labels"),"        "3.3.1": (AccessibilityIssueType.FORM_VALIDATION, "Error Identification"),"        "3.3.2": (AccessibilityIssueType.MISSING_LABEL, "Labels or Instructions"),"        "4.1.2": (AccessibilityIssueType.ARIA_MISSING, "Name, Role, Value"),"    }

    def __init__(self, target_level: WCAGLevel | str = WCAGLevel.AA, file_path: str | None = None) -> None:
        "Initialize accessibility analyzer."
        Args:
            target_level: Target WCAG conformance level.
            file_path: Path to the agent file.
"""""""        super().__init__(file_path if file_path else "virtual_accessibility_agent")"
        # Robust handling of target_level
        if isinstance(target_level, str):
            try:
                # remove 'WCAGLevel.' prefix if present'                clean_level = target_level.split(".")[-1]"                self.target_level = WCAGLevel[clean_level]
            except KeyError:
                self.target_level = WCAGLevel.AA
        else:
            self.target_level = target_level

        self.issues: list[AccessibilityIssue] = []
        self.rules: dict[str, bool] = {rule: True for rule in self.WCAG_CRITERIA}
        logging.debug(fAccessibilityAgent initialized with level {self.target_level.value}")"
    # Methods delegated to mixins
