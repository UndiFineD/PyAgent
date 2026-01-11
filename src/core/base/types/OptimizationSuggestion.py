#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from src.core.base.types.OptimizationType import OptimizationType

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
class OptimizationSuggestion:
    """A suggestion for code optimization.

    Attributes:
        type: Type of optimization.
        description: What to optimize.
        impact: Expected performance impact (low / medium / high).
        code_location: File and line information.
        before_snippet: Code before optimization.
        after_snippet: Suggested optimized code.
    """
    type: OptimizationType
    description: str
    impact: str
    code_location: str
    before_snippet: str = ""
    after_snippet: str = ""
