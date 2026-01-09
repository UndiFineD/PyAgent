#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .ConflictResolution import ConflictResolution

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
class MergeConflict:
    """Merge conflict information.

    Attributes:
        section: Section with conflict.
        ours: Our version of content.
        theirs: Their version of content.
        resolution: Applied resolution.
    """
    section: str
    ours: str
    theirs: str
    resolution: Optional[ConflictResolution] = None
