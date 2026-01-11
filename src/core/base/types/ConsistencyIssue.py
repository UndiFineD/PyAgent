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
class ConsistencyIssue:
    """A code consistency issue across the codebase.

    Attributes:
        issue_type: Type of inconsistency.
        description: Description of the issue.
        occurrences: List of file:line locations.
        recommended_style: The recommended consistent style.
    """
    issue_type: str
    description: str
    occurrences: List[str]
    recommended_style: str
