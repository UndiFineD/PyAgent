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


"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.types.accessibility_issue import AccessibilityIssue
from src.core.base.types.wcag_level import WCAGLevel
from dataclasses import dataclass, field

__version__ = VERSION


@dataclass
class AccessibilityReport:
    """Comprehensive accessibility report.

    Attributes:
        file_path: Path to analyzed file.
        issues: List of accessibility issues.
        total_elements: Total UI elements analyzed.
        wcag_level: Target WCAG level.
        compliance_score: Overall compliance score (0 - 100).
        critical_count: Number of critical issues.
        serious_count: Number of serious issues.
        recommendations: High - level recommendations.
    """

    file_path: str
    issues: list[AccessibilityIssue] = field(default_factory=lambda: [])
    total_elements: int = 0
    wcag_level: WCAGLevel = WCAGLevel.AA
    compliance_score: float = 100.0
    critical_count: int = 0
    serious_count: int = 0
    recommendations: list[str] = field(default_factory=lambda: [])
