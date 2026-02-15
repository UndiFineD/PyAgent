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

"""
CodeReviewerAgent - Automated code review

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- As a programmatic tool:
  from src.interface import CodeReviewerAgent
  reviewer = CodeReviewerAgent("path\\to\\file.py")
  findings = reviewer.review_code(source_text)
- As a CLI/tool endpoint: decorate review_code with as_tool for integration into the agent toolbox and pipeline.
- Typical input: a single string containing the full source file; output: list[ReviewFinding] objects with category, severity, line_number, message, suggestion, auto_fixable.

WHAT IT DOES:
- Performs automated, line-oriented code review for Python source text using:
  - Simple style checks (line length > 120 chars).
  - Regex-based pattern scanning for known anti-patterns and security smells (e.g., hardcoded passwords, range(len()) iteration).
  - Optional Rust-accelerated scanning (scan_lines_multi_pattern_rust) when rust_core is available, falling back to a Python scanner on ImportError or runtime failure.
  - Basic documentation checks to flag functions missing docstrings.
- Produces structured ReviewFinding results (category, message, line_number, severity, suggestion, auto_fixable) suitable for downstream reporting, triage, or automated help.
- Integrates with the BaseAgent lifecycle and is exposed as an as_tool callable for orchestration within the PyAgent swarm.

WHAT IT SHOULD DO BETTER:
- Broaden language/context awareness: current checks are line/regex-based and liable to false positives/negatives; add AST-based analysis (ast module) to detect issues with semantic accuracy and avoid matches inside strings/comments.
- Improve docstring detection to support single-line and multi-line docstrings robustly (current check is naive and only looks at the next line for triple quotes).
- Make severity/scoring and category assignment configurable and pluggable so projects can tune rules and thresholds.
- Add configurable auto-fix capabilities (and safe transactional file writes via StateTransaction) for low-risk style changes (e.g., line wrapping, replace range(len()) → enumerate()) and ensure fixes are reviewable by humans.
- Add richer security checks (taint analysis, credential detection across config patterns), dependency/version checks, and complexity/maintainability metrics (cyclomatic complexity).
- Improve reporting (group findings by file/function, include context lines, support SARIF or JSON output) and integrate with CI pipelines and code-review UIs.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_coder.py
"""

from __future__ import annotations

import re

from src.core.base.common.base_utilities import as_tool, create_main_function
from src.core.base.common.types.review_category import ReviewCategory
from src.core.base.common.types.review_finding import ReviewFinding
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

# Rust acceleration imports
try:
    from rust_core import scan_lines_multi_pattern_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

__version__ = VERSION


class CodeReviewerAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Automated code review system.

    Provides automated code review with actionable suggestions
    across multiple categories.

    Attributes:
        findings: List of review findings.

    Example:
        >>> reviewer=CodeReviewerAgent("path\\to\\agent.py")
        >>> findings=reviewer.review_code("def foo():\\n    pass")
    """

    # Pattern definitions for Rust acceleration
    REVIEW_PATTERNS = [
        (
            r'password\\s*=\\s*[\\\'"][^\\\'"]+[\\\'"]',
            ReviewCategory.SECURITY,
            5,
            "Potential hardcoded password",
            "Use environment variables or secure vault",
            False,
        ),
        (
            r"for\\s+\\w+\\s+in\\s+range\\(len\\(",
            ReviewCategory.PERFORMANCE,
            2,
            "Inefficient iteration pattern",
            "Use 'enumerate()' instead of 'range(len())'",
            True,
        ),
    ]

    def __init__(self, file_path: str | None = None) -> None:
        """Initialize the code reviewer."""
        super().__init__(file_path if file_path else "virtual_code_reviewer")
        self.findings: list[ReviewFinding] = []

    @as_tool(priority=5)
    def review_code(self, content: str) -> list[ReviewFinding]:
        """Perform automated code review.

        Args:
            content: Source code to review.

        Returns:
            List of review findings.
        """
        self.findings = []
        lines = content.split("\\n")

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
            except (RuntimeError, ValueError, TypeError, AttributeError):
                self._python_pattern_scan(lines)
        else:
            self._python_pattern_scan(lines)

        # Documentation checks (require context awareness)
        for i, line in enumerate(lines, 1):
            if re.match(r"^\\s*def\\s+[a-z_]\\w*\\s*\\(", line):
                if i < len(lines) and '\"\"\"' not in lines[i]:
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

    async def _process_task(self, task_data: dict) -> dict:
        """Process a task from the task queue.

        Args:
            task_data: Task dictionary with 'content' and optional 'target_file'.

        Returns:
            Dictionary with 'result' key containing the review report.
        """
        content = task_data.get("content", "")
        target_file = task_data.get("target_file")
        result = await self.improve_content(content, target_file)
        return {"result": result}

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Review code based on prompt or target file."""
        content = prompt
        if target_file:
            from pathlib import Path

            path = Path(target_file)
            if path.exists():
                content = path.read_text(encoding="utf-8")

        findings = self.review_code(content)
        if not findings:
            return "✅ No review findings. Code looks clean."

        report = ["## 🔍 Code Review Findings\n"]
        for f in findings:
            report.append(f"- [{f.category.name}] Line {f.line_number}: {f.message}")
            report.append(f"  * Suggestion: {f.suggestion}")

        return "\n".join(report)


if __name__ == "__main__":
    main = create_main_function(CodeReviewerAgent, "Code Reviewer", "Content to review")
    main()
