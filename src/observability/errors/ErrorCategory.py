#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_errors.py"""

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

class ErrorCategory(Enum):
    """Error categories."""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    TYPE = "type"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    DEPRECATION = "deprecation"
    VALUE = "value"
    IMPORT = "import"
    OTHER = "other"
