#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

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
class TestGap:
    """An identified gap in test coverage.

    Attributes:
        function_name: Name of the untested function.
        file_path: Path to the file containing the function.
        line_number: Line where the function is defined.
        complexity: Cyclomatic complexity of the function.
        suggested_tests: List of suggested test cases.
    """
    function_name: str
    file_path: str
    line_number: int
    complexity: int
    suggested_tests: List[str] = field(default_factory=lambda: [])
