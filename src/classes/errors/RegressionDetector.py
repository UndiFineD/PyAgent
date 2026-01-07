#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from .ErrorEntry import ErrorEntry
from .RegressionInfo import RegressionInfo

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess

class RegressionDetector:
    """Detects error regressions.

    Identifies errors that were previously fixed but have reappeared
    in the codebase.

    Attributes:
        fixed_errors: Map of fixed error signatures to commit info.
    """

    def __init__(self) -> None:
        """Initialize the regression detector."""
        self.fixed_errors: Dict[str, str] = {}  # signature -> fix_commit
        self.regressions: List[RegressionInfo] = []

    def record_fix(self, error: ErrorEntry, commit_hash: str) -> None:
        """Record that an error was fixed.

        Args:
            error: The fixed error.
            commit_hash: The commit that fixed the error.
        """
        signature = self._get_error_signature(error)
        self.fixed_errors[signature] = commit_hash

    def check_regression(
        self, error: ErrorEntry, current_commit: str = ""
    ) -> Optional[RegressionInfo]:
        """Check if an error is a regression.

        Args:
            error: The error to check.
            current_commit: Current commit hash.

        Returns:
            RegressionInfo if this is a regression, None otherwise.
        """
        signature = self._get_error_signature(error)
        if signature in self.fixed_errors:
            regression = RegressionInfo(
                error_id=error.id,
                original_fix_commit=self.fixed_errors[signature],
                regression_commit=current_commit
            )
            # Check if already tracked
            for r in self.regressions:
                if r.error_id == error.id:
                    r.occurrences += 1
                    return r
            self.regressions.append(regression)
            return regression
        return None

    def _get_error_signature(self, error: ErrorEntry) -> str:
        """Generate a signature for an error."""
        normalized = re.sub(r"\d+", "N", error.message)
        return f"{error.file_path}:{normalized}"

    def get_regressions(self) -> List[RegressionInfo]:
        """Get all detected regressions."""
        return self.regressions

    def get_regression_rate(self) -> float:
        """Calculate the regression rate."""
        if not self.fixed_errors:
            return 0.0
        return len(self.regressions) / len(self.fixed_errors) * 100
