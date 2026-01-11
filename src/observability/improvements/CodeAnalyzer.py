#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .Improvement import Improvement

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time


































from src.core.base.version import VERSION
__version__ = VERSION

class CodeAnalyzer:
    """Suggests analysis tools based on improvement content."""

    def __init__(self) -> None:
        self.tools: List[str] = [
            "security scan",
            "linter",
            "type checker",
            "coverage",
        ]

    def suggest_tools(self, improvement: Improvement) -> List[str]:
        text = f"{improvement.title} {improvement.description}".lower()
        suggestions: List[str] = []
        if "sql" in text or "injection" in text or "security" in text:
            suggestions.append("Security scan")
            suggestions.append("Dependency vulnerability scan")
        if "type" in text:
            suggestions.append("Type checker")
        if "test" in text:
            suggestions.append("Coverage")
        if not suggestions:
            suggestions.append("Linter")
        return suggestions
