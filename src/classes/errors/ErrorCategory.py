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
