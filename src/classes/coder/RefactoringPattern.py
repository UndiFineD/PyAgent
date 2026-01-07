#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .CodeLanguage import CodeLanguage

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
class RefactoringPattern:
    """A code refactoring pattern."""
    name: str
    description: str
    pattern: str
    replacement: str
    language: CodeLanguage = CodeLanguage.PYTHON
