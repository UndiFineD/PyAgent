#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from src.core.base.BaseAgent import BaseAgent
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

class AccessibilitySeverity(Enum):
    """Severity levels for accessibility issues."""
    CRITICAL = 4  # Blocks access for users with disabilities
    SERIOUS = 3   # Significant barrier to access
    MODERATE = 2  # Some difficulty for users
    MINOR = 1     # Cosmetic or minor inconvenience
