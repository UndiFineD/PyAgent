#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_errors.py"""

from .ErrorCategory import ErrorCategory
from .ErrorSeverity import ErrorSeverity

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class ErrorPattern:
    """A recognized error pattern."""
    name: str
    regex: str
    severity: ErrorSeverity
    category: ErrorCategory
    suggested_fix: str = ""
    occurrences: int = 0
