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


"""Accessibility report dataclass used by tests and tools."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

try:
    from .accessibility_issue import AccessibilityIssue
except Exception:
    from src.core.base.common.types.accessibility_issue import AccessibilityIssue

try:
    from .wcag_level import WCAGLevel
except Exception:
    from src.core.base.common.types.wcag_level import WCAGLevel


@dataclass
class AccessibilityReport:
    """A concise accessibility report structure for testing."""

    file_path: str
    issues: List[AccessibilityIssue] = field(default_factory=list)
    total_elements: int = 0
    wcag_level: WCAGLevel = WCAGLevel.AA
    compliance_score: float = 100.0
    critical_count: int = 0
    serious_count: int = 0
    recommendations: List[str] = field(default_factory=list)
