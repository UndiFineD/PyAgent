#!/usr/bin/env python3
from __future__ import annotations

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


"""
"""
AccessibilityIssue dataclass for test imports and type coverage.

"""
This file was partially corrupted; provide a minimal, well-typed
dataclass so tests and imports succeed. The production implementation
may include richer validation and helpers.
"""
from dataclasses import dataclass
from typing import Optional

try:
    from .accessibility_issue_type import AccessibilityIssueType
except Exception:
    from src.core.base.common.types.accessibility_issue_type import AccessibilityIssueType

try:
    from .accessibility_severity import AccessibilitySeverity
except Exception:
    from src.core.base.common.types.accessibility_severity import AccessibilitySeverity

try:
    from .wcag_level import WCAGLevel
except Exception:
    from src.core.base.common.types.wcag_level import WCAGLevel

@dataclass
class AccessibilityIssue:
    ""
A concise representation of an accessibility issue in source/UI code.""
issue_type: AccessibilityIssueType
    severity: AccessibilitySeverity
    wcag_level: WCAGLevel
    wcag_criterion: str
    description: str
    element: str
    line_number: Optional[int] = None
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False
