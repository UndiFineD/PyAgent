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
from src.core.base.types.OptimizationSuggestion import OptimizationSuggestion
from src.core.base.types.OptimizationType import OptimizationType
import re

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
        (r"for\s+\w+\s+in\s+range\(len\((\w+)\)\)", OptimizationType.ALGORITHMIC,
         "Use enumerate() instead of range(len())",
         "for idx, item in enumerate({0}):"),
        (r"\+=\s*.*?for\s+", OptimizationType.MEMORY,
         "String concatenation in loop is inefficient",
         "Use ''.join() or list comprehension"),
        (r"time\.sleep\(\d+\)", OptimizationType.CONCURRENCY,
         "Blocking sleep may hurt performance",
         "Consider asyncio.sleep() for async code"),
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
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            for pattern, opt_type, desc, fix in self.OPTIMIZATION_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    self.suggestions.append(OptimizationSuggestion(
                        type=opt_type,
                        description=desc,
                        impact="medium",
                        code_location=f"line {i}",
                        before_snippet=line.strip(),
                        after_snippet=fix.format(*match.groups()) if match.groups() else fix
                    ))

        return self.suggestions
