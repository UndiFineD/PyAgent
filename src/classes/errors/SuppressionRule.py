#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess

@dataclass
class SuppressionRule:
    """Rule for suppressing specific errors."""
    id: str
    pattern: str
    reason: str
    expires: Optional[str] = None
    created_by: str = ""
    created_at: str = ""
