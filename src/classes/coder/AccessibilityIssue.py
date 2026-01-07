#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .AccessibilityIssueType import AccessibilityIssueType
from .AccessibilitySeverity import AccessibilitySeverity
from .WCAGLevel import WCAGLevel

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
class AccessibilityIssue:
    """An accessibility issue found in UI code.

    Attributes:
        issue_type: Type of accessibility issue.
        severity: Severity level.
        wcag_level: WCAG conformance level affected.
        wcag_criterion: Specific WCAG criterion (e.g., "1.1.1").
        description: Human - readable description.
        element: UI element identifier or selector.
        line_number: Line number in source file.
        suggested_fix: Suggested fix for the issue.
        auto_fixable: Whether the issue can be auto - fixed.
    """
    issue_type: AccessibilityIssueType
    severity: AccessibilitySeverity
    wcag_level: WCAGLevel
    wcag_criterion: str
    description: str
    element: str
    line_number: Optional[int] = None
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False
