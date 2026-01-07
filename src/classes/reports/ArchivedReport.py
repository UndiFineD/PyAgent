#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

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

@dataclass
class ArchivedReport:
    """Archived report with retention info.
    Attributes:
        report_id: Unique report identifier.
        file_path: Original file path.
        content: Report content.
        archived_at: Archive timestamp.
        retention_days: Days to retain.
        metadata: Report metadata.
    """

    report_id: str
    file_path: str
    content: str
    archived_at: float = field(default_factory=time.time)  # type: ignore[assignment]
    retention_days: int = 90
    metadata: Dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
