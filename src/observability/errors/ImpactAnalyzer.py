#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_errors.py"""

from .ErrorEntry import ErrorEntry
from .ErrorImpact import ErrorImpact
from .ErrorSeverity import ErrorSeverity

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess


































from src.core.base.version import VERSION
__version__ = VERSION

class ImpactAnalyzer:
    """Analyzes the impact of errors on the codebase.

    Determines which files and functions are affected by errors
    and calculates impact scores.

    Attributes:
        file_dependencies: Map of file dependencies.
    """

    def __init__(self) -> None:
        """Initialize the impact analyzer."""
        self.file_dependencies: Dict[str, List[str]] = {}
        self.function_map: Dict[str, List[str]] = {}

    def add_dependency(self, file: str, depends_on: List[str]) -> None:
        """Add file dependencies.

        Args:
            file: The file path.
            depends_on: List of files this file depends on.
        """
        self.file_dependencies[file] = depends_on

    def add_functions(self, file: str, functions: List[str]) -> None:
        """Add functions in a file.

        Args:
            file: The file path.
            functions: List of function names in the file.
        """
        self.function_map[file] = functions

    def analyze(self, error: ErrorEntry) -> ErrorImpact:
        """Analyze the impact of an error.

        Args:
            error: The error to analyze.

        Returns:
            ErrorImpact with affected files and functions.
        """
        affected_files = self._find_affected_files(error.file_path)
        affected_functions = self.function_map.get(error.file_path, [])
        downstream = self._find_downstream_effects(error.file_path)

        impact_score = self._calculate_impact_score(
            len(affected_files),
            len(affected_functions),
            error.severity
        )

        return ErrorImpact(
            error_id=error.id,
            affected_files=affected_files,
            affected_functions=affected_functions,
            downstream_effects=downstream,
            impact_score=impact_score
        )

    def _find_affected_files(self, file_path: str) -> List[str]:
        """Find files that depend on the given file."""
        affected: List[str] = []
        for file, deps in self.file_dependencies.items():
            if file_path in deps:
                affected.append(file)
        return affected

    def _find_downstream_effects(self, file_path: str) -> List[str]:
        """Find downstream effects recursively."""
        effects: List[str] = []
        visited: Set[str] = set()
        self._find_downstream_recursive(file_path, effects, visited)
        return effects

    def _find_downstream_recursive(
        self, file_path: str, effects: List[str], visited: Set[str]
    ) -> None:
        """Recursively find downstream effects."""
        if file_path in visited:
            return
        visited.add(file_path)
        for file, deps in self.file_dependencies.items():
            if file_path in deps and file not in effects:
                effects.append(file)
                self._find_downstream_recursive(file, effects, visited)

    def _calculate_impact_score(
        self, file_count: int, func_count: int, severity: ErrorSeverity
    ) -> float:
        """Calculate an impact score."""
        base = severity.value * 10
        file_impact = min(file_count * 5, 30)
        func_impact = min(func_count * 2, 20)
        return min(100, base + file_impact + func_impact)
