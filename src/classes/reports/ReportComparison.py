#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

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
class ReportComparison:
    """Result of comparing two report versions.
    Attributes:
        old_path: Path to old version.
        new_path: Path to new version.
        added: Items added in new version.
        removed: Items removed from old version.
        changed: Items that changed (list of tuples of old, new).
        unchanged_count: Count of unchanged items.
    """

    old_path: str
    new_path: str
    added: List[str] = field(default_factory=list)  # type: ignore[assignment]
    removed: List[str] = field(default_factory=list)  # type: ignore[assignment]
    changed: List[tuple] = field(default_factory=list)  # type: ignore[assignment]
    unchanged_count: int = 0
