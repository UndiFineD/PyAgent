#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

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
