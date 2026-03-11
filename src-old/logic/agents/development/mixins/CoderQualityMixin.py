#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/CoderQualityMixin.description.md

# CoderQualityMixin

**File**: `src\\logic\agents\\development\\mixins\\CoderQualityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 122  
**Complexity**: 2 (simple)

## Overview

Quality scoring and refactoring suggestion logic for CoderCore.

## Classes (1)

### `CoderQualityMixin`

Mixin for computing quality scores and refactoring suggestions.

**Methods** (2):
- `calculate_quality_score(self, metrics, violations, smells, coverage)`
- `suggest_refactorings(self, content)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `src.core.base.types.CodeMetrics.CodeMetrics`
- `src.core.base.types.CodeSmell.CodeSmell`
- `src.core.base.types.QualityScore.QualityScore`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/CoderQualityMixin.improvements.md

# Improvements for CoderQualityMixin

**File**: `src\\logic\agents\\development\\mixins\\CoderQualityMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 122 lines (medium)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoderQualityMixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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

from typing import Any, Dict, List

from src.core.base.types.CodeMetrics import CodeMetrics
from src.core.base.types.CodeSmell import CodeSmell
from src.core.base.types.QualityScore import QualityScore


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
            score.issues.append(
                f"Style: {violation['message']} (line {violation['line']})"
            )
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
                        "description": (
                            f"Create a data class for parameters at "
                            f"line {smell.line_number}"
                        ),
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
                    "description": (
                        f"Extract {len(duplicates)} duplicate code blocks "
                        f"into shared methods"
                    ),
                    "reason": f"Found {len(duplicates)} duplicate code patterns",
                }
            )
        return suggestions
