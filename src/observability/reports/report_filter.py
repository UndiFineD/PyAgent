#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .CodeIssue import CodeIssue
from .FilterCriteria import FilterCriteria

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

class ReportFilter:
    """Filters reports based on criteria.
    Attributes:
        criteria: Filter criteria to apply.
    """

    def __init__(self, criteria: Optional[FilterCriteria] = None) -> None:
        """Initialize filter.
        Args:
            criteria: Filter criteria. Uses defaults if not provided.
        """

        self.criteria = criteria or FilterCriteria()

    def matches(self, issue: CodeIssue) -> bool:
        """Check if issue matches filter criteria.
        Args:
            issue: Code issue to check.
        Returns:
            True if issue matches all criteria.
        """

        # Check severity
        if self.criteria.min_severity and issue.severity.value < self.criteria.min_severity.value:
            return False
        # Check category
        if self.criteria.categories and issue.category not in self.criteria.categories:
            return False
        return True

    def filter_issues(self, issues: List[CodeIssue]) -> List[CodeIssue]:
        """Filter list of issues.
        Args:
            issues: List of issues to filter.
        Returns:
            Filtered list of issues.
        """

        return [i for i in issues if self.matches(i)]
