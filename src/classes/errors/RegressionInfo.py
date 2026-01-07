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
class RegressionInfo:
    """Information about error regression.

    Attributes:
        error_id: ID of the regressed error.
        original_fix_commit: Commit that originally fixed the error.
        regression_commit: Commit that reintroduced the error.
        occurrences: Number of times this error has regressed.
    """
    error_id: str
    original_fix_commit: str = ""
    regression_commit: str = ""
    occurrences: int = 1
