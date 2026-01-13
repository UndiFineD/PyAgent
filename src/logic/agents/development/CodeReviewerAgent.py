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
from src.core.base.types.ReviewCategory import ReviewCategory
from src.core.base.types.ReviewFinding import ReviewFinding
from typing import Dict, List
import re

__version__ = VERSION

class CodeReviewer:
    """Automated code review system.

    Provides automated code review with actionable suggestions
    across multiple categories.

    Attributes:
        findings: List of review findings.

    Example:
        >>> reviewer=CodeReviewer()
        >>> findings=reviewer.review_code("def foo():\\n    pass")
    """

    def __init__(self) -> None:
        """Initialize the code reviewer."""
        self.findings: List[ReviewFinding] = []

    def review_code(self, content: str) -> List[ReviewFinding]:
        """Perform automated code review.

        Args:
            content: Source code to review.

        Returns:
            List of review findings.
        """
        self.findings = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Style checks
            if len(line) > 120:
                self.findings.append(ReviewFinding(
                    category=ReviewCategory.STYLE,
                    message=f"Line exceeds 120 characters ({len(line)})",
                    line_number=i,
                    severity=2,
                    suggestion="Break line into multiple lines",
                    auto_fixable=False
                ))

            # Security checks
            if re.search(r'password\s*=\s*[\'"][^\'"]+[\'"]', line, re.I):
                self.findings.append(ReviewFinding(
                    category=ReviewCategory.SECURITY,
                    message="Potential hardcoded password",
                    line_number=i,
                    severity=5,
                    suggestion="Use environment variables or secure vault",
                    auto_fixable=False
                ))

            # Performance checks
            if re.search(r"for\s+\w+\s+in\s+range\(len\(", line):
                self.findings.append(ReviewFinding(
                    category=ReviewCategory.PERFORMANCE,
                    message="Inefficient iteration pattern",
                    line_number=i,
                    severity=2,
                    suggestion="Use 'enumerate()' instead of 'range(len())'",
                    auto_fixable=True
                ))

            # Documentation checks
            if re.match(r"^\s*def\s+[a-z_]\w*\s*\(", line):
                # Check for docstring on next line
                if i < len(lines) and '"""' not in lines[i]:
                    self.findings.append(ReviewFinding(
                        category=ReviewCategory.DOCUMENTATION,
                        message="Function missing docstring",
                        line_number=i,
                        severity=3,
                        suggestion="Add docstring describing function purpose",
                        auto_fixable=False
                    ))

        return self.findings

    def get_summary(self) -> Dict[str, int]:
        """Get summary of findings by category.

        Returns:
            Dictionary mapping category to count.
        """
        summary: Dict[str, int] = {}
        for finding in self.findings:
            cat = finding.category.value
            summary[cat] = summary.get(cat, 0) + 1
        return summary