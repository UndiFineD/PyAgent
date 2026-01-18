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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .ErrorEntry import ErrorEntry
from .FixSuggestion import FixSuggestion
from typing import Dict, List, Optional
import re

__version__ = VERSION

class AutoFixSuggester:
    """Generates automated fix suggestions for errors.

    Uses pattern matching and common fixes to suggest
    resolutions for errors.

    Attributes:
        fix_patterns: Map of error patterns to fix templates.
    """

    def __init__(self) -> None:
        """Initialize the auto-fix suggester."""
        self.fix_patterns: dict[str, str] = {
            r"NameError: name '(\w+)' is not defined":
                "Define variable '{0}' before use or import it",
            r"ImportError: No module named '(\w+)'":
                "Install module with: pip install {0}",
            r"TypeError: unsupported operand type":
                "Check operand types and convert if necessary",
            r"AttributeError: '(\w+)' object has no attribute '(\w+)'":
                "Check if '{1}' exists on {0} object or use hasattr()",
            r"IndexError: list index out of range":
                "Check list bounds before accessing index",
            r"KeyError: '(\w+)'":
                "Use .get('{0}', default) or check key existence",
        }

    def add_pattern(self, pattern: str, fix_template: str) -> None:
        """Add a fix pattern.

        Args:
            pattern: Regex pattern to match errors.
            fix_template: Template for the fix suggestion.
        """
        self.fix_patterns[pattern] = fix_template

    def suggest(self, error: ErrorEntry) -> FixSuggestion | None:
        """Generate a fix suggestion for an error.

        Args:
            error: The error to fix.

        Returns:
            FixSuggestion if a fix is available, None otherwise.
        """
        for pattern, template in self.fix_patterns.items():
            match = re.search(pattern, error.message)
            if match:
                groups = match.groups()
                suggestion = template.format(*groups) if groups else template
                return FixSuggestion(
                    error_id=error.id,
                    suggestion=suggestion,
                    confidence=0.8,
                    source="pattern_match"
                )
        return None

    def suggest_all(
        self, errors: list[ErrorEntry]
    ) -> list[FixSuggestion]:
        """Generate suggestions for multiple errors."""
        suggestions: list[FixSuggestion] = []
        for error in errors:
            sugg = self.suggest(error)
            if sugg:
                suggestions.append(sugg)
        return suggestions