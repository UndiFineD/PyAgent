#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from src.core.base.BaseAgent import BaseAgent
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
class ContextVersion:
    """Version information for context."""
    version: str
    timestamp: str
    content_hash: str
    changes: List[str] = field(default_factory=lambda: [])
    author: str = ""
