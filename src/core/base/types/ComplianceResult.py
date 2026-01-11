#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .ComplianceCategory import ComplianceCategory

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

@dataclass
class ComplianceResult:
    """Result of compliance checking.

    Attributes:
        category: Compliance category checked.
        passed: Whether the check passed.
        issues: List of compliance issues found.
        recommendations: Recommendations for fixing issues.
    """
    category: ComplianceCategory
    passed: bool
    issues: List[str] = field(default_factory=lambda: [])
    recommendations: List[str] = field(default_factory=lambda: [])
