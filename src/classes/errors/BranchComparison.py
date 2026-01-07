#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

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

@dataclass
class BranchComparison:
    """Comparison of errors across branches.

    Attributes:
        branch_a: First branch name.
        branch_b: Second branch name.
        errors_only_in_a: Error IDs only in branch A.
        errors_only_in_b: Error IDs only in branch B.
        common_errors: Error IDs in both branches.
    """
    branch_a: str
    branch_b: str
    errors_only_in_a: List[str] = field(default_factory=lambda: [])
    errors_only_in_b: List[str] = field(default_factory=lambda: [])
    common_errors: List[str] = field(default_factory=lambda: [])
