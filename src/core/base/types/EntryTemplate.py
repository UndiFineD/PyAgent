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
class EntryTemplate:
    """Template for changelog entries with placeholders.

    Attributes:
        name: Template name.
        template_text: Template with placeholders.
        placeholders: List of placeholder names.
        description: Description of the template.
    """
    name: str
    template_text: str
    placeholders: List[str] = field(default_factory=lambda: [])
    description: str = ""
