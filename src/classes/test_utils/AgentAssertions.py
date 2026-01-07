#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .TestAssertion import TestAssertion

from typing import List
import json
import re

class AgentAssertions:
    """Custom assertion helpers for agent testing.

    Example:
        assertions=AgentAssertions()
        assertions.assert_valid_python("print('hello')")
        assertions.assert_markdown_structure(content, headers=True)
    """

    def __init__(self) -> None:
        """Initialize assertion helpers."""
        self._assertions: List[TestAssertion] = []

    def assert_valid_python(self, code: str) -> bool:
        """Assert code is valid Python.

        Args:
            code: Python code to validate.

        Returns:
            bool: True if valid.

        Raises:
            AssertionError: If invalid Python.
        """
        try:
            compile(code, "<string>", "exec")
            assertion = TestAssertion(
                name="valid_python",
                expected="valid",
                actual="valid",
                passed=True,
            )
            self._assertions.append(assertion)
            return True
        except SyntaxError as e:
            assertion = TestAssertion(
                name="valid_python",
                expected="valid",
                actual=f"invalid: {e}",
                passed=False,
            )
            self._assertions.append(assertion)
            raise AssertionError(f"Invalid Python: {e}")

    def assert_contains_docstring(self, code: str) -> bool:
        """Assert code contains docstrings.

        Args:
            code: Python code to check.

        Returns:
            bool: True if contains docstrings.
        """
        has_docstring = '"""' in code or "'''" in code
        assertion = TestAssertion(
            name="contains_docstring",
            expected=True,
            actual=has_docstring,
            passed=has_docstring,
        )
        self._assertions.append(assertion)

        if not has_docstring:
            raise AssertionError("Code does not contain docstrings")
        return True

    def assert_markdown_structure(
        self,
        content: str,
        headers: bool = True,
        code_blocks: bool = False,
    ) -> bool:
        """Assert markdown has expected structure.

        Args:
            content: Markdown content.
            headers: Expect headers.
            code_blocks: Expect code blocks.

        Returns:
            bool: True if structure matches.
        """
        issues: List[str] = []
        if headers and not re.search(r"^#+\s", content, re.MULTILINE):
            issues.append("missing headers")
        if code_blocks and "```" not in content:
            issues.append("missing code blocks")
        passed = len(issues) == 0
        assertion = TestAssertion(
            name="markdown_structure",
            expected="valid structure",
            actual=", ".join(issues) if issues else "valid",
            passed=passed,
        )
        self._assertions.append(assertion)
        if not passed:
            raise AssertionError(f"Markdown structure issues: {', '.join(issues)}")
        return True

    def assert_json_valid(self, content: str) -> bool:
        """Assert content is valid JSON.

        Args:
            content: JSON content.

        Returns:
            bool: True if valid JSON.
        """
        try:
            json.loads(content)
            assertion = TestAssertion(
                name="json_valid",
                expected="valid",
                actual="valid",
                passed=True,
            )
            self._assertions.append(assertion)
            return True
        except json.JSONDecodeError as e:
            assertion = TestAssertion(
                name="json_valid",
                expected="valid",
                actual=f"invalid: {e}",
                passed=False,
            )
            self._assertions.append(assertion)
            raise AssertionError(f"Invalid JSON: {e}")

    def get_assertions(self) -> List[TestAssertion]:
        """Get all recorded assertions."""
        return list(self._assertions)
