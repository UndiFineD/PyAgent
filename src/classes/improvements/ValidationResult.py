#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .ValidationSeverity import ValidationSeverity

from base_agent import BaseAgent
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

@dataclass
class ValidationResult:
    """Result from improvement validation.

    Attributes:
        improvement_id: ID of the validated improvement.
        is_valid: Whether the improvement passed validation.
        issues: List of validation issues.
        test_results: Results from automated tests.
    """
    improvement_id: str
    is_valid: bool = True
    issues: List[Tuple[ValidationSeverity, str]] = field(
        default_factory=lambda: []
    )
    test_results: Dict[str, bool] = field(
        default_factory=lambda: {}  # type: ignore[assignment]
    )

    @property
    def errors(self) -> List[str]:
        """Compatibility accessor used by tests."""
        return [msg for sev, msg in self.issues if sev == ValidationSeverity.ERROR]
