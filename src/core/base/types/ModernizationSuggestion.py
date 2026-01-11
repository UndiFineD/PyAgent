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
class ModernizationSuggestion:
    """Suggestion to modernize deprecated API usage.

    Attributes:
        old_api: The deprecated API being used.
        new_api: The modern replacement API.
        deprecation_version: Version where the old API was deprecated.
        removal_version: Version where it will be removed.
        migration_guide: URL or text explaining migration.
    """
    old_api: str
    new_api: str
    deprecation_version: str
    removal_version: Optional[str] = None
    migration_guide: str = ""
