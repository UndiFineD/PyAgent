#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from base_agent import BaseAgent
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
class ContextTemplate:
    """Template for context documentation."""
    name: str
    file_type: str
    sections: List[str]
    template_content: str
    required_fields: List[str] = field(default_factory=lambda: [])
