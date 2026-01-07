#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

@dataclass
class ValidationResult:
    """Result of report validation.
    Attributes:
        valid: Whether report is valid.
        errors: Validation errors.
        warnings: Validation warnings.
        checksum: Content checksum.
    """

    valid: bool
    errors: List[str] = field(default_factory=list)  # type: ignore[assignment]
    warnings: List[str] = field(default_factory=list)  # type: ignore[assignment]
    checksum: str = ""
