#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from src.logic.agents.cognitive.context.models.InheritanceMode import InheritanceMode

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
class InheritedContext:
    """Inherited context from parent file.

    Attributes:
        parent_path: Path to parent context file.
        inherited_sections: Sections inherited from parent.
        mode: Inheritance mode used.
        overrides: Sections that override parent.
    """
    parent_path: str
    inherited_sections: List[str] = field(default_factory=lambda: [])
    mode: InheritanceMode = InheritanceMode.MERGE
    overrides: List[str] = field(default_factory=lambda: [])
