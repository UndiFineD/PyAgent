#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .Improvement import Improvement
from .ImprovementDiffType import ImprovementDiffType

from src.core.base.BaseAgent import BaseAgent
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


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class ImprovementDiff:
    """Difference in a single improvement between branches.

    Attributes:
        improvement_id: Unique improvement identifier.
        diff_type: Type of difference.
        source_version: Improvement in source branch (if exists).
        target_version: Improvement in target branch (if exists).
        change_summary: Summary of changes.
    """
    improvement_id: str
    diff_type: ImprovementDiffType
    source_version: Optional[Improvement] = None
    target_version: Optional[Improvement] = None
    change_summary: str = ""
