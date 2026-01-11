#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

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
class DiffResult:
    """Result of a changelog diff comparison.

    Attributes:
        additions: Lines added.
        deletions: Lines removed.
        modifications: Lines changed.
        unchanged: Lines unchanged.
        similarity_score: Percentage of similarity (0 - 100).
    """
    additions: List[str] = field(default_factory=lambda: [])
    deletions: List[str] = field(default_factory=lambda: [])
    modifications: List[Tuple[str, str]] = field(default_factory=lambda: [])
    unchanged: int = 0
    similarity_score: float = 0.0
