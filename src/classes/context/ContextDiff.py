#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from src.classes.base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

@dataclass
class ContextDiff:
    """Diff between context versions.

    Attributes:
        version_from: Source version.
        version_to: Target version.
        added_sections: List of added sections.
        removed_sections: List of removed sections.
        modified_sections: List of modified section names.
        change_summary: Brief summary of changes.
    """
    version_from: str
    version_to: str
    added_sections: List[str] = field(default_factory=lambda: [])
    removed_sections: List[str] = field(default_factory=lambda: [])
    modified_sections: List[str] = field(default_factory=lambda: [])
    change_summary: str = ""
