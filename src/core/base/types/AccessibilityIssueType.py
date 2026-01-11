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

class AccessibilityIssueType(Enum):
    """Types of accessibility issues in UI code."""
    MISSING_ALT_TEXT = "missing_alt_text"
    LOW_COLOR_CONTRAST = "low_color_contrast"
    MISSING_LABEL = "missing_label"
    KEYBOARD_NAVIGATION = "keyboard_navigation"
    FOCUS_MANAGEMENT = "focus_management"
    ARIA_MISSING = "aria_missing"
    ARIA_INVALID = "aria_invalid"
    HEADING_HIERARCHY = "heading_hierarchy"
    FORM_VALIDATION = "form_validation"
    SEMANTIC_HTML = "semantic_html"
