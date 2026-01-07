#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from .ErrorCategory import ErrorCategory
from .ErrorSeverity import ErrorSeverity

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
class ErrorPattern:
    """A recognized error pattern."""
    name: str
    regex: str
    severity: ErrorSeverity
    category: ErrorCategory
    suggested_fix: str = ""
    occurrences: int = 0
