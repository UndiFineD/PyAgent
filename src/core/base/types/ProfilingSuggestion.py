#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from src.core.base.types.ProfilingCategory import ProfilingCategory

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
class ProfilingSuggestion:
    """A code profiling suggestion.

    Attributes:
        category: Category of the profiling suggestion.
        function_name: Function that could benefit from profiling.
        reason: Why this function should be profiled.
        estimated_impact: Estimated performance impact.
        profiling_approach: Suggested profiling approach.
    """
    category: ProfilingCategory
    function_name: str
    reason: str
    estimated_impact: str
    profiling_approach: str
