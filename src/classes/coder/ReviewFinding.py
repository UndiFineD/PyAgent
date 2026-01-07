#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .ReviewCategory import ReviewCategory

from base_agent import BaseAgent
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile

@dataclass
class ReviewFinding:
    """A finding from automated code review.

    Attributes:
        category: Category of the finding.
        message: Description of the issue.
        line_number: Line where the issue was found.
        severity: Severity level (1 - 5).
        suggestion: Suggested fix.
        auto_fixable: Whether this can be auto - fixed.
    """
    category: ReviewCategory
    message: str
    line_number: int
    severity: int
    suggestion: str
    auto_fixable: bool = False
