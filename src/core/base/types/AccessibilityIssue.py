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
from src.core.base.types.AccessibilityIssueType import AccessibilityIssueType
from src.core.base.types.AccessibilitySeverity import AccessibilitySeverity
from src.core.base.types.WCAGLevel import WCAGLevel
from dataclasses import dataclass
from typing import Optional

__version__ = VERSION

@dataclass
class AccessibilityIssue:
    """An accessibility issue found in UI code.

    Attributes:
        issue_type: Type of accessibility issue.
        severity: Severity level.
        wcag_level: WCAG conformance level affected.
        wcag_criterion: Specific WCAG criterion (e.g., "1.1.1").
        description: Human - readable description.
        element: UI element identifier or selector.
        line_number: Line number in source file.
        suggested_fix: Suggested fix for the issue.
        auto_fixable: Whether the issue can be auto - fixed.
    """
    issue_type: AccessibilityIssueType
    severity: AccessibilitySeverity
    wcag_level: WCAGLevel
    wcag_criterion: str
    description: str
    element: str
    line_number: Optional[int] = None
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False