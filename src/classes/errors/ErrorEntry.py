#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from .ErrorCategory import ErrorCategory
from .ErrorSeverity import ErrorSeverity

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
class ErrorEntry:
    """A single error entry."""
    id: str = ""
    message: str = ""
    file_path: str = ""
    line_number: int = 0
    # Compatibility: older tests/callers pass error_type.
    error_type: str = ""
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.OTHER
    timestamp: str = ""
    stack_trace: str = ""
    suggested_fix: str = ""
    resolved: bool = False
    resolution_timestamp: str = ""
    tags: List[str] = field(default_factory=lambda: [])

    def __post_init__(self) -> None:
        if not self.id:
            seed = f"{self.error_type}|{self.message}|{self.file_path}|{self.line_number}".encode("utf-8")
            self.id = hashlib.sha256(seed).hexdigest()[:12]

        if self.error_type and self.category == ErrorCategory.OTHER:
            et = self.error_type.lower()
            if "security" in et or "auth" in et:
                self.category = ErrorCategory.SECURITY
            elif "type" in et:
                self.category = ErrorCategory.TYPE
            elif "syntax" in et:
                self.category = ErrorCategory.SYNTAX
            elif "value" in et:
                self.category = ErrorCategory.VALUE
            elif "import" in et:
                self.category = ErrorCategory.IMPORT
