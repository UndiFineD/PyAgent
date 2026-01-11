#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from generate_agent_reports.py"""

from .ReportType import ReportType

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
class ReportSearchResult:
    """Result from report search.
    Attributes:
        file_path: Path to report file.
        report_type: Type of report.
        match_text: Matched text snippet.
        line_number: Line number of match.
        score: Relevance score.
    """

    file_path: str
    report_type: ReportType
    match_text: str
    line_number: int
    score: float = 1.0
