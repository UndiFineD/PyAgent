#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .RefactoringSuggestion import RefactoringSuggestion

from src.classes.base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

class RefactoringAdvisor:
    """Suggests refactoring based on context analysis.

    Analyzes context to suggest code refactoring opportunities.

    Example:
        >>> advisor=RefactoringAdvisor()
        >>> suggestions=advisor.analyze(contexts)
    """

    def __init__(self) -> None:
        self.patterns: Dict[str, Dict[str, str]] = {}

    def add_pattern(self, name: str, pattern: str, description: str) -> None:
        """Add a custom refactoring pattern.

        Args:
            name: Pattern identifier.
            pattern: Regex pattern to search for.
            description: Human-readable suggestion description.
        """
        self.patterns[name] = {"pattern": pattern, "description": description}

    def analyze(self, contexts: Any) -> List[RefactoringSuggestion]:
        """Analyze contexts for refactoring opportunities.

        Args:
            contexts: Either a single context string or a dictionary of
                context file paths to contents.

        Returns:
            List of refactoring suggestions.
        """
        context_map: Dict[str, str]
        if isinstance(contexts, str):
            context_map = {"inline": contexts}
        elif isinstance(contexts, dict):
            context_map = contexts  # type: ignore
        else:
            raise TypeError("contexts must be a string or a dict")

        suggestions: List[RefactoringSuggestion] = []

        # Apply custom patterns first.
        for path, content in context_map.items():
            for name, spec in self.patterns.items():
                try:
                    if re.search(spec["pattern"], content):
                        suggestions.append(RefactoringSuggestion(
                            suggestion_type=name,
                            description=spec.get("description", ""),
                            affected_files=[path],
                            estimated_impact="low",
                        ))
                except re.error:
                    # Invalid user-provided regex; ignore for robustness.
                    continue

        # Look for duplicate descriptions (indicating code duplication)
        descriptions: Dict[str, List[str]] = {}
        for path, content in context_map.items():
            purpose = re.search(r"##\s*Purpose\s*\n(.+?)(?=##|\Z)", content, re.DOTALL)
            if purpose:
                desc = purpose.group(1).strip()[:100]
                if desc not in descriptions:
                    descriptions[desc] = []
                descriptions[desc].append(path)
        for desc, files in descriptions.items():
            if len(files) > 1:
                suggestions.append(RefactoringSuggestion(
                    suggestion_type="extract_common",
                    description=f"Similar purpose found in {len(files)} files",
                    affected_files=files,
                    estimated_impact="medium"
                ))
        return suggestions

    def prioritize(self, suggestions: List[RefactoringSuggestion]) -> List[RefactoringSuggestion]:
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
