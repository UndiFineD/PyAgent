#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/agent/AgentRefactorMixin.description.md

# AgentRefactorMixin

**File**: `src\\logic\agents\\development\\mixins\agent\\AgentRefactorMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 75  
**Complexity**: 5 (moderate)

## Overview

Refactoring pattern and duplication logic for CoderAgent.

## Classes (1)

### `AgentRefactorMixin`

Mixin for code deduplication and refactoring patterns.

**Methods** (5):
- `find_duplicate_code(self, content, min_lines)`
- `get_duplicate_ratio(self, content)`
- `add_refactoring_pattern(self, pattern)`
- `apply_refactoring_patterns(self, content)`
- `suggest_refactorings(self, content)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `re`
- `src.core.base.types.RefactoringPattern.RefactoringPattern`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/agent/AgentRefactorMixin.improvements.md

# Improvements for AgentRefactorMixin

**File**: `src\\logic\agents\\development\\mixins\agent\\AgentRefactorMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 75 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentRefactorMixin_test.py` with pytest tests

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

"""Refactoring pattern and duplication logic for CoderAgent."""

import re
from typing import Any

from src.core.base.types.RefactoringPattern import RefactoringPattern


class AgentRefactorMixin:
    """Mixin for code deduplication and refactoring patterns."""

    def find_duplicate_code(
        self, content: str | None = None, min_lines: int = 4
    ) -> list[dict[str, Any]]:
        """Find duplicate code blocks."""
        if content is None:
            content = (
                getattr(self, "current_content", "")
                or getattr(self, "previous_content", "")
                or ""
            )
        if hasattr(self, "core"):
            return self.core.find_duplicate_code(content, min_lines)
        return []

    def get_duplicate_ratio(self, content: str | None = None) -> float:
        """Calculate the ratio of duplicate code."""
        if content is None:
            content = (
                getattr(self, "current_content", "")
                or getattr(self, "previous_content", "")
                or ""
            )
        duplicates = self.find_duplicate_code(content)
        total_lines = len(content.split("\n"))
        if total_lines == 0:
            return 0.0
        duplicate_lines = sum(
            (d["occurrences"] - 1) * 4 for d in duplicates  # min_lines default
        )
        return min(1.0, duplicate_lines / total_lines)

    def add_refactoring_pattern(self, pattern: RefactoringPattern) -> None:
        """Add a refactoring pattern."""
        if not hasattr(self, "_refactoring_patterns"):
            self._refactoring_patterns = []
        self._refactoring_patterns.append(pattern)

    def apply_refactoring_patterns(self, content: str) -> tuple[str, list[str]]:
        """Apply all registered refactoring patterns."""
        result = content
        applied: list[str] = []
        patterns = getattr(self, "_refactoring_patterns", [])
        for pattern in patterns:
            if pattern.language != getattr(self, "_language", None):
                continue
            new_result = re.sub(pattern.pattern, pattern.replacement, result)
            if new_result != result:
                applied.append(pattern.name)
                result = new_result
        return result, applied

    def suggest_refactorings(self, content: str | None = None) -> list[dict[str, str]]:
        """Suggest possible refactorings based on code analysis."""
        if content is None:
            content = (
                getattr(self, "current_content", "")
                or getattr(self, "previous_content", "")
                or ""
            )
        if hasattr(self, "core"):
            return self.core.suggest_refactorings(content)
        return []
