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
class ErrorImpact:
    """Impact analysis for an error.

    Attributes:
        error_id: ID of the analyzed error.
        affected_files: List of files affected by the error.
        affected_functions: Functions impacted by the error.
        downstream_effects: Downstream components affected.
        impact_score: Overall impact score (0 - 100).
    """
    error_id: str
    affected_files: List[str] = field(default_factory=lambda: [])
    affected_functions: List[str] = field(default_factory=lambda: [])
    downstream_effects: List[str] = field(default_factory=lambda: [])
    impact_score: float = 0.0
