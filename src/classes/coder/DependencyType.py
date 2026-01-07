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

class DependencyType(Enum):
    """Types of code dependencies."""
    IMPORT = "import"
    FUNCTION_CALL = "function_call"
    CLASS_INHERITANCE = "class_inheritance"
    VARIABLE_REFERENCE = "variable_reference"
