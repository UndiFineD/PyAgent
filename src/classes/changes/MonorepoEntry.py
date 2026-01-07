#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .ChangelogEntry import ChangelogEntry

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

@dataclass
class MonorepoEntry:
    """Changelog entry for monorepo aggregation.

    Attributes:
        package_name: Name of the package.
        version: Package version.
        entries: List of changelog entries for this package.
        path: Path to the package in the repo.
    """
    package_name: str
    version: str
    entries: List[ChangelogEntry] = field(default_factory=lambda: [])
    path: str = ""
