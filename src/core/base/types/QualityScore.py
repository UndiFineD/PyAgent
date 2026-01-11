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

@dataclass
class QualityScore:
    """Code quality score with breakdown."""
    overall_score: float = 0.0
    maintainability: float = 0.0
    readability: float = 0.0
    complexity: float = 0.0
    documentation: float = 0.0
    test_coverage: float = 0.0
    issues: List[str] = field(default_factory=lambda: [])

    @property
    def score(self) -> float:
        """Compatibility alias for overall_score."""
        return self.overall_score

    @score.setter
    def score(self, value: float) -> None:
        self.overall_score = value
