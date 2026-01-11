#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from src.core.base.types.AccessibilityIssue import AccessibilityIssue
from src.core.base.types.WCAGLevel import WCAGLevel

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

@dataclass
class AccessibilityReport:
    """Comprehensive accessibility report.

    Attributes:
        file_path: Path to analyzed file.
        issues: List of accessibility issues.
        total_elements: Total UI elements analyzed.
        wcag_level: Target WCAG level.
        compliance_score: Overall compliance score (0 - 100).
        critical_count: Number of critical issues.
        serious_count: Number of serious issues.
        recommendations: High - level recommendations.
    """
    file_path: str
    issues: List[AccessibilityIssue] = field(default_factory=lambda: [])
    total_elements: int = 0
    wcag_level: WCAGLevel = WCAGLevel.AA
    compliance_score: float = 100.0
    critical_count: int = 0
    serious_count: int = 0
    recommendations: List[str] = field(default_factory=lambda: [])
