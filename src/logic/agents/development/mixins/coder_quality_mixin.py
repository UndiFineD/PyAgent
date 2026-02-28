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
Quality scoring and refactoring suggestion logic for CoderCore.
"""

# pylint: disable=too-many-ancestors

from __future__ import annotations

from typing import Any, Dict, List

from src.core.base.common.types.code_metrics import CodeMetrics
from src.core.base.common.types.code_smell import CodeSmell
from src.core.base.common.types.quality_score import QualityScore


class CoderQualityMixin:
    """Mixin for computing quality scores and refactoring suggestions."""

    def calculate_quality_score(
        self,
        metrics: CodeMetrics,
        violations: List[Dict[str, Any]],
        smells: List[CodeSmell],
        coverage: float,
    ) -> QualityScore:
        """Aggregate all analysis into a single QualityScore."""
        score = QualityScore()
        score.maintainability = min(100, metrics.maintainability_index)

        # Readability score
        readability_deductions = len(violations) * 5
        score.readability = max(0, 100 - readability_deductions)

        # Complexity score
        if metrics.function_count > 0:
            avg_cc = metrics.cyclomatic_complexity / metrics.function_count
            score.complexity = max(0, 100 - (avg_cc - 1) * 10)
        else:
            score.complexity = 100

        # Documentation score
        if metrics.lines_of_code > 0:
            comment_ratio = metrics.lines_of_comments / metrics.lines_of_code
            score.documentation = min(100, comment_ratio * 200)

        score.test_coverage = coverage

        # Overall score (weighted average)
        score.overall_score = (
            score.maintainability * 0.25
            + score.readability * 0.25
            + score.complexity * 0.25
            + score.documentation * 0.15
            + score.test_coverage * 0.10
        )

        # Add primary issues
        for violation in violations[:5]:
            score.issues.append(f"Style: {violation['message']} (line {violation['line']})")
        for smell in smells[:5]:
            score.issues.append(f"Smell: {smell.description}")

        return score

    def suggest_refactorings(self, content: str) -> List[Dict[str, str]]:
        """Suggest possible refactorings based on code analysis."""
        suggestions: List[Dict[str, str]] = []
        # Detect code smells and suggest refactorings
        smells = self.detect_code_smells(content)
        for smell in smells:
            if smell.name == "long_method":
                suggestions.append(
                    {
                        "type": "extract_method",
                        "description": f"Extract parts of method at line {smell.line_number}",
                        "reason": smell.description,
                    }
                )
            elif smell.name == "too_many_parameters":
                suggestions.append(
                    {
                        "type": "introduce_parameter_object",
                        "description": (f"Create a data class for parameters at line {smell.line_number}"),
                        "reason": smell.description,
                    }
                )
            elif smell.name == "god_class":
                suggestions.append(
                    {
                        "type": "extract_class",
                        "description": f"Split class at line {smell.line_number} into focused classes",
                        "reason": smell.description,
                    }
                )
        # Check for duplicate code
        duplicates = self.find_duplicate_code(content)
        if duplicates:
            suggestions.append(
                {
                    "type": "extract_method",
                    "description": (f"Extract {len(duplicates)} duplicate code blocks into shared methods"),
                    "reason": f"Found {len(duplicates)} duplicate code patterns",
                }
            )
        return suggestions
