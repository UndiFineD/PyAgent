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
class ReportMetadata:
    """Metadata for a generated report.
    Attributes:
        path: Path to source file.
        generated_at: Timestamp of generation.
        content_hash: SHA256 hash of content.
        version: Report version string.
    """

    path: str
    generated_at: str
    content_hash: str
    version: str
