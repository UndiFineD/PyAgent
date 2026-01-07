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
