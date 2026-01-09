#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from src.classes.base_agent import BaseAgent
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
class GeneratedCode:
    """Context-aware generated code.

    Attributes:
        language: Programming language.
        code: Generated code content.
        context_used: Context files used for generation.
        description: Description of what the code does.
    """
    language: str
    code: str
    context_used: List[str] = field(default_factory=lambda: [])
    description: str = ""
