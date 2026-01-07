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
class ChangelogEntry:
    """A single changelog entry."""
    category: str
    description: str
    version: str = ""
    date: str = ""
    priority: int = 0  # Higher=more important
    severity: str = "normal"  # low, normal, high, critical
    tags: List[str] = field(default_factory=lambda: [])
    linked_issues: List[str] = field(default_factory=lambda: [])
    linked_commits: List[str] = field(default_factory=lambda: [])
