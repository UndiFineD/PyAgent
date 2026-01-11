#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from src.core.base.types.DependencyType import DependencyType

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
class DependencyNode:
    """A node in the dependency graph.

    Attributes:
        name: Name of the module / class / function.
        type: Type of dependency.
        depends_on: List of dependencies.
        depended_by: List of dependents.
        file_path: Path to the file.
    """
    name: str
    type: DependencyType
    depends_on: List[str] = field(default_factory=lambda: [])
    depended_by: List[str] = field(default_factory=lambda: [])
    file_path: str = ""
