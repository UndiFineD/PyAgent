#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from generate_agent_reports.py"""

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


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class CodeIssue:
    """Represents a code issue or improvement suggestion.
    Attributes:
        message: Issue description.
        category: Issue category.
        severity: Severity level.
        line_number: Line number if applicable.
        file_path: File path if applicable.
        function_name: Function name if applicable.
    """

    message: str
    category: IssueCategory
    severity: SeverityLevel = SeverityLevel.INFO
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    function_name: Optional[str] = None
