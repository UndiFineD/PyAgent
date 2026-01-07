#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .CodeIssue import CodeIssue

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
class AggregatedReport:
    """Report aggregated from multiple sources.
    Attributes:
        sources: Source report paths.
        combined_issues: Combined issues from all sources.
        summary: Aggregation summary.
        generated_at: Generation timestamp.
    """

    sources: List[str] = field(default_factory=list)  # type: ignore[assignment]
    combined_issues: List[CodeIssue] = field(default_factory=list)  # type: ignore[assignment]
    summary: Dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
    generated_at: float = field(default_factory=time.time)  # type: ignore[assignment]
