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

@dataclass
class FixSuggestion:
    """Automated fix suggestion for an error.

    Attributes:
        error_id: ID of the error to fix.
        suggestion: The suggested fix.
        confidence: Confidence score (0 - 1).
        code_snippet: Example code for the fix.
        source: Source of the suggestion.
    """
    error_id: str
    suggestion: str
    confidence: float = 0.0
    code_snippet: str = ""
    source: str = "pattern_match"
