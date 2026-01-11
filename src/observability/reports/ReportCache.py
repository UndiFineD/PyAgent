#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from generate_agent_reports.py"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class ReportCache:
    """Cache for report data.
    Attributes:
        path: File path for the cached report.
        content_hash: Hash of the cached content.
        content: The cached report content.
        created_at: Timestamp when cache was created.
        ttl_seconds: Time - to - live for cache entries.
    """

    path: str = ""
    content_hash: str = ""
    content: str = ""
    created_at: float = 0.0
    ttl_seconds: int = 3600
