#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from src.core.base.BaseAgent import BaseAgent
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


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class MergeCandidate:
    """Candidate for merging with another improvement.

    Attributes:
        source_id: ID of the source improvement.
        target_id: ID of the target improvement.
        similarity_score: How similar the improvements are.
        merge_reason: Why these should be merged.
    """
    source_id: str
    target_id: str
    similarity_score: float = 0.0
    merge_reason: str = ""
