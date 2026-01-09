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

class InheritanceMode(Enum):
    """Modes for context inheritance."""
    OVERRIDE = "override"
    MERGE = "merge"
    APPEND = "append"
