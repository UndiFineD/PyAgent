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

"""Refactoring pattern and duplication logic for CoderAgent."""

# pylint: disable=too-many-ancestors

from __future__ import annotations

import re
from typing import Any

from src.core.base.common.types.refactoring_pattern import RefactoringPattern


class AgentRefactorMixin:
    """Mixin for code deduplication and refactoring patterns."""

    def find_duplicate_code(self, content: str | None = None, min_lines: int = 4) -> list[dict[str, Any]]:
        """Find duplicate code blocks."""
        if content is None:
            content = getattr(self, "current_content", "") or getattr(self, "previous_content", "") or ""
        if hasattr(self, "core"):
            return self.core.find_duplicate_code(content, min_lines)
        return []

    def get_duplicate_ratio(self, content: str | None = None) -> float:
        """Calculate the ratio of duplicate code."""
        if content is None:
            content = getattr(self, "current_content", "") or getattr(self, "previous_content", "") or ""
        duplicates = self.find_duplicate_code(content)
        total_lines = len(content.split("\n"))
        if total_lines == 0:
            return 0.0
        duplicate_lines = sum(
            (d["occurrences"] - 1) * 4  # min_lines default
            for d in duplicates
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
            content = getattr(self, "current_content", "") or getattr(self, "previous_content", "") or ""
        if hasattr(self, "core"):
            return self.core.suggest_refactorings(content)
        return []
