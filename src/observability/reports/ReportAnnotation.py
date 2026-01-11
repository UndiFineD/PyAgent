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
class ReportAnnotation:
    """Annotation on a report.
    Attributes:
        annotation_id: Unique annotation identifier.
        report_id: Associated report ID.
        author: Author of annotation.
        content: Annotation content.
        line_number: Line number if applicable.
        created_at: Creation timestamp.
    """

    annotation_id: str
    report_id: str
    author: str
    content: str
    line_number: Optional[int] = None
    created_at: float = field(default_factory=time.time)  # type: ignore[assignment]
