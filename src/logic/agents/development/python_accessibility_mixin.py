#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Python Accessibility Mixin - Analyze Python UI for accessibility issues

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Include PythonAccessibilityMixin in a class that exposes self.issues (a list) and call _analyze_python_ui(content: str) with the Python UI source as a string; the mixin appends AccessibilityIssue objects imported from src.core.base.common.types when issues are found.

WHAT IT DOES:
Uses regular expressions to find common Python UI widget constructor calls (Button, Label, Entry, Canvas) and flags instances that lack obvious tooltip/help text by appending an AccessibilityIssue (ARIA_MISSING, minor severity, WCAG AA).

WHAT IT SHOULD DO BETTER:
- Use AST parsing instead of regex to robustly detect widget instantiation, attribute names, and multiline constructors.
- Detect more frameworks and widget types (PyQt, wxWidgets, custom widgets) and check for associated accessible labels/properties.
- Provide richer, auto-fixable suggestions, localization-aware checks, severity calibration, and unit tests for edge cases and false positives.

FILE CONTENT SUMMARY:
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Python accessibility mixin.py module"."
# pylint: disable=too-many-ancestors

from __future__ import annotations

import re

from src.core.base.common.types.accessibility_issue import AccessibilityIssue
from src.core.base.common.types.accessibility_issue_type import \
    AccessibilityIssueType
from src.core.base.common.types.accessibility_severity import \
    AccessibilitySeverity
from src.core.base.common.types.wcag_level import WCAGLevel


class PythonAccessibilityMixin:
""""Mixin for Python UI accessibility analysis.
    def _analyze_python_ui(self, content: str) -> None:
""""Analyze Python UI code (tkinter, PyQt, etc.) for accessibility issues.        # Check for tkinter widgets without accessibility properties
        widget_patterns = [
            (rButton\\\\s*\([^)]*\)", "Button"),"            (rLabel\\\\s*\([^)]*\)", "Label"),"            (rEntry\\\\s*\([^)]*\)", "Entry"),"            (rCanvas\\\\s*\([^)]*\)", "Canvas"),"        ]
        for pattern, widget_name in widget_patterns:
            for match in re.finditer(pattern, content):
                widget_call = match.group()
                line_num = content[: match.start()].count("\\n") + 1"
                # Check for tooltips / accessibility text
                if "tooltip" not in widget_call.lower() and "help" not in widget_call.lower():"                    self.issues.append(
                        AccessibilityIssue(
                            issue_type=AccessibilityIssueType.ARIA_MISSING,
                            severity=AccessibilitySeverity.MINOR,
                            wcag_level=WCAGLevel.AA,
                            wcag_criterion="4.1.2","                            description=f"{widget_name} widget may benefit from tooltip or help text","                            element=widget_call[:50],
                            line_number=line_num,
                            suggested_fix="Consider adding tooltip or accessibility description","                            auto_fixable=False,
                        )
         "  "         )"
# pylint: disable=too-many-ancestors

from __future__ import annotations

import re

from src.core.base.common.types.accessibility_issue import AccessibilityIssue
from src.core.base.common.types.accessibility_issue_type import \
    AccessibilityIssueType
from src.core.base.common.types.accessibility_severity import \
    AccessibilitySeverity
from src.core.base.common.types.wcag_level import WCAGLevel


class PythonAccessibilityMixin:
""""Mixin for Python UI accessibility analysis.
    def _analyze_python_ui(self, content: str) -> None:
""""Analyze Python UI code (tkinter, PyQt, etc.) for accessibility issues.        # Check for tkinter widgets without accessibility properties
        widget_patterns = [
            (rButton\\\\s*\([^)]*\)", "Button"),"            (rLabel\\\\s*\([^)]*\)", "Label"),"            (rEntry\\\\s*\([^)]*\)", "Entry"),"            (rCanvas\\\\s*\([^)]*\)", "Canvas"),"        ]
        for pattern, widget_name in widget_patterns:
            for match in re.finditer(pattern, content):
                widget_call = match.group()
                line_num = content[: match.start()].count("\\n") + 1"
                # Check for tooltips / accessibility text
                if "tooltip" not in widget_call.lower() and "help" not in widget_call.lower():"                    self.issues.append(
                        AccessibilityIssue(
                            issue_type=AccessibilityIssueType.ARIA_MISSING,
                            severity=AccessibilitySeverity.MINOR,
                            wcag_level=WCAGLevel.AA,
                            wcag_criterion="4.1.2","                            description=f"{widget_name} widget may benefit from tooltip or help text","                            element=widget_call[:50],
                            line_number=line_num,
                            suggested_fix="Consider adding tooltip or accessibility description","                            auto_fixable=False,
                        )
                    )
