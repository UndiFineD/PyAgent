#!/usr/bin/env python3
"""PerformanceAgent identifies and suggests code optimizations."""

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

from __future__ import annotations

import logging
import re

# Try to import rust acceleration
try:
    from rust_core import \
        scan_optimization_patterns_rust  # pylint: disable=no-name-in-module

    HAS_RUST_CORE = True
except ImportError:
    HAS_RUST_CORE = False

from src.core.base.common.types.optimization_suggestion import \
    OptimizationSuggestion
from src.core.base.common.types.optimization_type import OptimizationType
from src.core.base.lifecycle.version import VERSION

logger = logging.getLogger(__name__)

__version__ = VERSION


class PerformanceAgent:
    """Identifies and suggests code optimizations.

    Analyzes code for performance bottlenecks and suggests
    improvements.

    Attributes:
        suggestions: List of optimization suggestions.

    Example:
        >>> optimizer=PerformanceAgent()
        >>> suggestions=optimizer.analyze("for i in range(len(items)):")
    """

    OPTIMIZATION_PATTERNS: list[tuple[str, OptimizationType, str, str]] = [
        (
            r"for\s+\w+\s+in\s+range\(len\((\w+)\)\)",
            OptimizationType.ALGORITHMIC,
            "Use enumerate() instead of range(len())",
            "for idx, item in enumerate({0}):",
        ),
        (
            r"\+=\s*.*?for\s+",
            OptimizationType.MEMORY,
            "String concatenation in loop is inefficient",
            "Use ''.join() or list comprehension",
        ),
        (
            r"time\.sleep\(\d+\)",
            OptimizationType.CONCURRENCY,
            "Blocking sleep may hurt performance",
            "Consider asyncio.sleep() for async code",
        ),
    ]

    def __init__(self) -> None:
        """Initialize the performance optimizer."""
        self.suggestions: list[OptimizationSuggestion] = []

    def analyze(self, content: str) -> list[OptimizationSuggestion]:
        """Analyze code for optimization opportunities.

        Args:
            content: Source code to analyze.

        Returns:
            List of optimization suggestions.
        """
        self.suggestions = []

        if HAS_RUST_CORE:
            try:
                rust_results = scan_optimization_patterns_rust(content)
                if rust_results:
                    for line_num, pattern_idx, groups in rust_results:
                        if pattern_idx < len(self.OPTIMIZATION_PATTERNS):
                            pattern, opt_type, desc, fix = self.OPTIMIZATION_PATTERNS[pattern_idx]
                            self.suggestions.append(
                                OptimizationSuggestion(
                                    type=opt_type,
                                    description=desc,
                                    impact="medium",
                                    code_location=f"line {line_num}",
                                    before_snippet="",
                                    after_snippet=fix.format(*groups) if groups else fix,
                                )
                            )
                    return self.suggestions
            except (ImportError, AttributeError, RuntimeError) as e:
                logger.debug("Rust acceleration failed: %s", e)

        # Fallback to Python implementation
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            for pattern, opt_type, desc, fix in self.OPTIMIZATION_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    self.suggestions.append(
                        OptimizationSuggestion(
                            type=opt_type,
                            description=desc,
                            impact="medium",
                            code_location=f"line {i}",
                            before_snippet=line.strip(),
                            after_snippet=fix.format(*match.groups()) if match.groups() else fix,
                        )
                    )

        return self.suggestions
