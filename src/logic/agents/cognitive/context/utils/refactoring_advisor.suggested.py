#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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


"""Refactoring advice engine for Cognitive agents.

This module analyzes agent contexts to identify potential refactoring
opportunities and suggestions, leveraging Rust acceleration when available.
"""

from __future__ import annotations
import re
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.context.models.refactoring_suggestion import (
    RefactoringSuggestion,
)

try:
    from rust_core import apply_patterns_rust

    _RUST_ACCEL = True
except ImportError:
    _RUST_ACCEL = False

__version__ = VERSION


class RefactoringAdvisor:
    """Suggests refactoring based on context analysis.

    Analyzes context to suggest code refactoring opportunities.

    Example:
        >>> advisor = RefactoringAdvisor()
        >>> suggestions = advisor.analyze(contexts)
    """

    def __init__(self) -> None:
        """Initialize refactoring advisor."""
        self.patterns: dict[str, dict[str, str]] = {}

    def add_pattern(self, name: str, pattern: str, description: str) -> None:
        """Add a custom refactoring pattern.

        Args:
            name: Pattern identifier.
            pattern: Regex pattern to search for.
            description: Human-readable suggestion description.
        """
        self.patterns[name] = {"pattern": pattern, "description": description}

    def analyze(self, contexts: Any) -> list[RefactoringSuggestion]:
        """Analyze contexts for refactoring opportunities.

        Args:
            contexts: Either a single context string or a dictionary of
                context file paths to contents.

        Returns:
            List of refactoring suggestions.
        """
        context_map: dict[str, str]
        if isinstance(contexts, str):
            context_map = {"inline": contexts}
        elif isinstance(contexts, dict):
            context_map = contexts  # type: ignore
        else:
            raise TypeError("contexts must be a string or a dict")

        suggestions: list[RefactoringSuggestion] = []

        # Apply custom patterns first.
        if _RUST_ACCEL and self.patterns:
            # Use Rust for pattern matching: Vec<(path, content)>, Vec<(name, pattern)>
            content_list = list(context_map.items())
            pattern_list = [(name, spec["pattern"]) for name, spec in self.patterns.items()]
            matches = apply_patterns_rust(content_list, pattern_list)
            for path, name in matches:
                spec = self.patterns[name]
                suggestions.append(
                    RefactoringSuggestion(
                        suggestion_type=name,
                        description=spec.get("description", ""),
                        affected_files=[path],
                        estimated_impact="low",
                    )
                )
        else:
            for path, content in context_map.items():
                for name, spec in self.patterns.items():
                    try:
                        if re.search(spec["pattern"], content):
                            suggestions.append(
                                RefactoringSuggestion(
                                    suggestion_type=name,
                                    description=spec.get("description", ""),
                                    affected_files=[path],
                                    estimated_impact="low",
                                )
                            )
                    except re.error:
                        # Invalid user-provided regex; ignore for robustness.
                        continue

        # Look for duplicate descriptions (indicating code duplication)
        descriptions: dict[str, list[str]] = {}
        for path, content in context_map.items():
            purpose = re.search(r"##\s*Purpose\s*\n(.+?)(?=##|\Z)", content, re.DOTALL)
            if purpose:
                desc = purpose.group(1).strip()[:100]
                if desc not in descriptions:
                    descriptions[desc] = []
                descriptions[desc].append(path)
        for desc, files in descriptions.items():
            if len(files) > 1:
                suggestions.append(
                    RefactoringSuggestion(
                        suggestion_type="extract_common",
                        description=f"Similar purpose found in {len(files)} files",
                        affected_files=files,
                        estimated_impact="medium",
                    )
                )
        return suggestions

    def prioritize(self, suggestions: list[RefactoringSuggestion]) -> list[RefactoringSuggestion]:
        """Prioritize refactoring suggestions.

        Args:
            suggestions: Suggestions to prioritize.

        Returns:
            Suggestions sorted by estimated impact.
        """
        impact_rank = {"high": 0, "medium": 1, "low": 2}

        def rank(s: RefactoringSuggestion) -> int:
            return impact_rank.get(getattr(s, "estimated_impact", "medium"), 1)

        return sorted(list(suggestions), key=rank)
