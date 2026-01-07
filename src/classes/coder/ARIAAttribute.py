#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

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
class ARIAAttribute:
    """ARIA attribute definition.

    Attributes:
        name: ARIA attribute name (e.g., "aria-label").
        value: Current value.
        is_valid: Whether the value is valid.
        allowed_values: List of allowed values (if constrained).
        suggestion: Suggested improvement.
    """
    name: str
    value: str = ""
    is_valid: bool = True
    allowed_values: List[str] = field(default_factory=lambda: [])
    suggestion: Optional[str] = None
