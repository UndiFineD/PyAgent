#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .IssueCategory import IssueCategory
from .SeverityLevel import SeverityLevel

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

@dataclass
class FilterCriteria:
    """Criteria for filtering reports.
    Attributes:
        date_from: Start date for filtering.
        date_to: End date for filtering.
        min_severity: Minimum severity level.
        categories: Categories to include.
        file_patterns: Glob patterns for files.
    """

    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_severity: Optional[SeverityLevel] = None
    categories: Optional[List[IssueCategory]] = None
    file_patterns: Optional[List[str]] = None
