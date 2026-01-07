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
class ContextRecommendation:
    """Recommendation for context improvement.

    Attributes:
        source_file: File used as reference.
        suggested_sections: Sections to add.
        reason: Why this recommendation was made.
        confidence: Recommendation confidence.
    """
    source_file: str
    suggested_sections: List[str] = field(default_factory=lambda: [])
    reason: str = ""
    confidence: float = 0.0
