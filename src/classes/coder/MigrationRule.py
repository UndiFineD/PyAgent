#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .MigrationStatus import MigrationStatus

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
class MigrationRule:
    """A rule for code migration from old to new API.

    Attributes:
        name: Rule identifier.
        old_pattern: Regex pattern to match old API usage.
        new_pattern: Replacement pattern for new API.
        description: Human - readable description of the migration.
        status: Current status of this migration rule.
        breaking_change: Whether this is a breaking change.
    """
    name: str
    old_pattern: str
    new_pattern: str
    description: str
    status: MigrationStatus = MigrationStatus.PENDING
    breaking_change: bool = False
