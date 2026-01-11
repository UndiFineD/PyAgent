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
class CodeMetrics:
    """Code quality metrics."""
    lines_of_code: int = 0
    lines_of_comments: int = 0
    blank_lines: int = 0
    cyclomatic_complexity: float = 0.0
    maintainability_index: float = 100.0
    function_count: int = 0
    class_count: int = 0
    import_count: int = 0
    average_function_length: float = 0.0
    max_function_length: int = 0
    duplicate_code_ratio: float = 0.0
