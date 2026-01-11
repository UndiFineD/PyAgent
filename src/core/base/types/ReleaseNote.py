#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

@dataclass
class ReleaseNote:
    """Generated release notes.

    Attributes:
        version: Release version.
        title: Release title.
        summary: Brief summary.
        highlights: Key highlights.
        breaking_changes: List of breaking changes.
        full_changelog: Complete changelog text.
    """
    version: str
    title: str
    summary: str
    highlights: List[str] = field(default_factory=lambda: [])
    breaking_changes: List[str] = field(default_factory=lambda: [])
    full_changelog: str = ""
