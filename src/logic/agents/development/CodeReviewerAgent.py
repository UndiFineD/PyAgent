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
from src.core.base.Version import VERSION
from src.core.base.types.ReviewCategory import ReviewCategory
from src.core.base.types.ReviewFinding import ReviewFinding
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool
import re

# Rust acceleration imports
try:
    from rust_core import scan_lines_multi_pattern_rust
    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

__version__ = VERSION


class CodeReviewerAgent(BaseAgent):
    """Automated code review system.

    Provides automated code review with actionable suggestions
    across multiple categories.

    Attributes:
        findings: List of review findings.

    Example:
        >>> reviewer=CodeReviewerAgent("path/to/agent.py")
        >>> findings=reviewer.review_code("def foo():\\n    pass")
    """

    # Pattern definitions for Rust acceleration
    REVIEW_PATTERNS = [
        (r'password\s*=\s*[\'"][^\'"]+[\'"]', ReviewCategory.SECURITY, 5,
         "Potential hardcoded password", "Use environment variables or secure vault", False),
        (r"for\s+\w+\s+in\s+range\(len\(", ReviewCategory.PERFORMANCE, 2,
         "Inefficient iteration pattern", "Use 'enumerate()' instead of 'range(len())'", True),
    ]

    def __init__(self, file_path: str | None = None) -> None:
        """Initialize the code reviewer."""
        super().__init__(file_path if file_path else "virtual_code_reviewer")
        self.findings: list[ReviewFinding] = []

    @as_tool
    def review_code(self, content: str) -> list[ReviewFinding]:
        """Perform automated code review.

        Args:
            content: Source code to review.

        Returns:
            List of review findings.
        """
        self.findings = []
        lines = content.split("\n")

        # Line length checks (simple, no regex needed)
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self.findings.append(
                    ReviewFinding(
                        category=ReviewCategory.STYLE,
                        message=f"Line exceeds 120 characters ({len(line)})",
                        line_number=i,
                        severity=2,
                        suggestion="Break line into multiple lines",
                        auto_fixable=False,
                    )
                )

        # Rust-accelerated pattern scanning
        if _RUST_AVAILABLE:
            try:
                patterns = [p[0] for p in self.REVIEW_PATTERNS]
                matches = scan_lines_multi_pattern_rust(content, patterns)
                for line_num, pat_idx, _ in matches:
                    _, category, severity, message, suggestion, auto_fix = self.REVIEW_PATTERNS[pat_idx]
                    self.findings.append(
                        ReviewFinding(
                            category=category,
                            message=message,
                            line_number=line_num,
                            severity=severity,
                            suggestion=suggestion,
                            auto_fixable=auto_fix,
                        )
                    )
            except Exception:
                self._python_pattern_scan(lines)
        else:
            self._python_pattern_scan(lines)

        # Documentation checks (require context awareness)
        for i, line in enumerate(lines, 1):
            if re.match(r"^\s*def\s+[a-z_]\w*\s*\(", line):
                if i < len(lines) and '"""' not in lines[i]:
                    self.findings.append(
                        ReviewFinding(
                            category=ReviewCategory.DOCUMENTATION,
                            message="Function missing docstring",
                            line_number=i,
                            severity=3,
                            suggestion="Add docstring describing function purpose",
                            auto_fixable=False,
                        )
                    )

        return self.findings

    def _python_pattern_scan(self, lines: list[str]) -> None:
        """Python fallback for pattern scanning."""
        for i, line in enumerate(lines, 1):
            # Security checks
            if re.search(r'password\s*=\s*[\'"][^\'"]+[\'"]', line, re.I):
                self.findings.append(
                    ReviewFinding(
                        category=ReviewCategory.SECURITY,
                        message="Potential hardcoded password",
                        line_number=i,
                        severity=5,
                        suggestion="Use environment variables or secure vault",
                        auto_fixable=False,
                    )
                )

            # Performance checks
            if re.search(r"for\s+\w+\s+in\s+range\(len\(", line):
                self.findings.append(
                    ReviewFinding(
                        category=ReviewCategory.PERFORMANCE,
                        message="Inefficient iteration pattern",
                        line_number=i,
                        severity=2,
                        suggestion="Use 'enumerate()' instead of 'range(len())'",
                        auto_fixable=True,
                    )
                )

    def get_summary(self) -> dict[str, int]:
        """Get summary of findings by category.

        Returns:
            Dictionary mapping category to count.
        """
        summary: dict[str, int] = {}
        for finding in self.findings:
            cat = finding.category.value
            summary[cat] = summary.get(cat, 0) + 1
        return summary
