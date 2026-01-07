#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time

class ImprovementDiffType(Enum):
    """Types of improvement differences between branches."""
    ADDED = "added"      # Improvement exists only in target branch
    REMOVED = "removed"  # Improvement exists only in source branch
    MODIFIED = "modified"  # Improvement exists in both but changed
    UNCHANGED = "unchanged"  # Improvement is identical in both
