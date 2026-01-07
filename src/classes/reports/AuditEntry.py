#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .AuditAction import AuditAction

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
class AuditEntry:
    """Audit log entry.
    Attributes:
        entry_id: Unique entry identifier.
        timestamp: Event timestamp.
        action: Audit action.
        user_id: User who performed action.
        report_id: Affected report.
        details: Additional details.
    """

    entry_id: str
    timestamp: float
    action: AuditAction
    user_id: str
    report_id: str
    details: Dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
