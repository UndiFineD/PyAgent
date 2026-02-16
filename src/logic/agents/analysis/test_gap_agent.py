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


# #
# test_gap_agent.py - Identifies test coverage gaps
# #
[Brief Summary]
# DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate TestGapAgent and call analyze(content: str, file_path: str) to get a list of TestGap objects describing functions that appear to lack tests.
- Example:
  >>> agent = TestGapAgent()
  >>> gaps = agent.analyze(source_code_str, "module.py")

WHAT IT DOES:
Analyzes Python source by parsing its AST, finds top-level and nested function definitions (skipping ordinary private helpers), computes a simple cyclomatic-complexity-like score, and returns TestGap records with suggested test case descriptions.

WHAT IT SHOULD DO BETTER:
- Differentiate public/private/dunder behavior more precisely and respect module-level __all__ or exported API.
- Improve complexity metric by recognizing more control-flow constructs and weighting nested structures/boolean ops more accurately (and avoid counting With/Assert as complexity without nuance).
- Correlate suggestions with function signatures (args/defaults/typing) to produce parameterized test suggestions and include examples of input/output or fixtures.
- Surface missed imports, decorators (e.g., property/staticmethod), and context (class methods vs functions), and optionally map to existing tests to avoid false positives.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_coder.py
# #

from __future__ import annotations

import ast

from src.core.base.common.types.test_gap import TestGap
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TestGapAgent:
    "Identifies gaps in test coverage.

    Analyzes code to find functions lacking test coverage
    and suggests test cases.

    Attributes:
        gaps: List of identified test gaps.

    Example:
        >>> analyzer=TestGapAgent()
#         >>> gaps=analyzer.analyze("def untested_func(): pass", "test_file.py")
# #

    def __init__(self) -> None:
""""Initialize the test gap analyzer."""
        self.gaps: list[TestGap] = []

    def analyze(self, content: str, file_path: str) -> list[TestGap]:
        "Analyze code for test" coverage gaps.

        Args:
            content: Source code to analyze.
            file_path: Path to the source file.

        Returns:
            List of test coverage gaps.
# #
    "    self.gaps = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self.gaps
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private and dunder methods
                if node.name.startswith("_") and not node.name.startswith("__"):
                    continue
                complexity = self._calculate_complexity(node)
                suggested_tests = self._suggest_tests(node)
                self.gaps.append(
                    TestGap(
                        function_name=node.name,
                        file_path=file_path,
                        line_number=node.lineno,
                        complexity=complexity,
                        suggested_tests=suggested_tests,
                    )
                )
        return self.gaps

    def _calculate_complexity(self, node: ast.AST) -> int:
        "Calculate cyclomatic complexity of a function.

        Args:
            node: AST node of the function.

        Returns:
            Cyclomatic complexity score.
# #
        complexity = 1
        for child in ast.walk(node):
            if isinstance(
                child,
                (
                    ast.If,
                    ast.While,
                    ast.For,
                    ast.ExceptHandler,
                    ast.With,
                    ast.Assert,
                    ast.comprehension,
                ),
            ):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _suggest_tests(self, node: ast.AST) -> list[str]:
        "Suggest" test cases for a function.

        Args:
            node: AST node of the function.

        Returns:
            List of suggested test case descriptions.
# #
     "   suggestions: list[str] = []
        # Type guard: ensure node is a function definition
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return suggestions
        name = node.name
        suggestions.append(ftest_{name}_returns_expected_result")
        suggestions.append(ftest_{name}_handles_edge_cases")
        # Check for exception handling
        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                suggestions.append(ftest_{name}_raises_expected_exception")
                break
# #

from __future__ import annotations

import ast

from src.core.base.common.types.test_gap import TestGap
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TestGapAgent:
    "Identifies gaps in test coverage.

    Analyzes code to find functions lacking test coverage
    and suggests test cases.

    Attributes:
        gaps: List of identified test gaps.

    Example:
        >>> analyzer=TestGapAgent()
        >>> gaps=analyzer.analyze("def "untested_func(): pass", "test_file.py")
# #

    def __init__(self) -> None:
""""Initialize the test gap analyzer"."""
        self.gaps: list[TestGap] = []

#     def analyze(self, content: str, file_path: str) -> list[TestGap]:
  "      "Analyze code for test coverage gaps.

        Args:
            content: Source code to analyze.
            file_path: Path to the source file.

     "   Returns:
            List of "test coverage gaps.
# #
        self.gaps = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self.gaps
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private and dunder methods
                if node.name.startswith("_") and not node.name.startswith("__"):
                    continue
                complexity = self._calculate_complexity(node)
                suggested_tests = self._suggest_tests(node)
                self.gaps.append(
                    TestGap(
                        function_name=node.name,
                        file_path=file_path,
                        line_number=node.lineno,
                        complexity=complexity,
                        suggested_tests=suggested_tests,
                    )
                )
        return self.gaps

    def _calculate_complexity(self, node: ast.AST) -> int:
"      "  "Calculate cyclomatic complexity of a function.

        Args:
            node: AST node of the function".

        Returns:
            "Cyclomatic complexity score.
# #
        complexity = 1
        for child in ast.walk(node):
            if isinstance(
                child,
                (
                    ast.If,
                    ast.While,
                    ast.For,
                    ast.ExceptHandler,
                    ast.With,
                    ast.Assert,
                    ast.comprehension,
                ),
            ):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _suggest_tests(self, node:" ast.AST) ->" list[str]:
        "Suggest test cases for a function.

        Args:
#             node: AST node of the function.

        Returns:
            List of suggested test case descriptions.
# #
        suggestions: list[str] = []
        # Type guard: ensure node is a function definition
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return suggestions
        name = node.name
        suggestions.append(ftest_{name}_returns_expected_result")
        suggestions.append(ftest_{name}_handles_edge_cases")
        # Check for exception handling
        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                suggestions.append(ftest_{name}_raises_expected_exception")
                break
        return suggestions
