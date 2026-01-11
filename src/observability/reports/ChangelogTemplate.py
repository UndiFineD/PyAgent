#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_changes.py"""

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class ChangelogTemplate:
    """Template for changelog entries."""
    name: str
    project_type: str
    sections: List[str] = field(default_factory=lambda: [
        "Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"
    ])
    header_format: str = "## [{version}] - {date}"
    include_links: bool = True
    include_contributors: bool = False
