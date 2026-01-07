#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .BranchComparisonStatus import BranchComparisonStatus
from .ImprovementDiff import ImprovementDiff

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time

@dataclass
class BranchComparison:
    """Result of comparing improvements across branches.

    Attributes:
        source_branch: Source branch name.
        target_branch: Target branch name.
        file_path: Path to improvements file.
        status: Comparison status.
        diffs: List of improvement differences.
        added_count: Number of improvements added.
        removed_count: Number of improvements removed.
        modified_count: Number of improvements modified.
        compared_at: Comparison timestamp.
    """
    source_branch: str
    target_branch: str
    file_path: str
    status: BranchComparisonStatus = BranchComparisonStatus.PENDING
    diffs: List[ImprovementDiff] = field(default_factory=list)  # type: ignore[assignment]
    added_count: int = 0
    removed_count: int = 0
    modified_count: int = 0
    compared_at: float = field(default_factory=time.time)
