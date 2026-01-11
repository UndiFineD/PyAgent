#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from src.core.base.types.CodeLanguage import CodeLanguage
from src.core.base.types.StyleRuleSeverity import StyleRuleSeverity

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
class StyleRule:
    """A configurable code style rule."""
    name: str
    pattern: str
    message: str
    severity: StyleRuleSeverity = StyleRuleSeverity.WARNING
    enabled: bool = True
    language: Optional[CodeLanguage] = None
    auto_fix: Optional[Callable[[str], str]] = None
