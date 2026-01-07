#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .PermissionLevel import PermissionLevel

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
class ReportPermission:
    """Permission for report access.
    Attributes:
        user_id: User identifier.
        report_pattern: Glob pattern for reports.
        level: Permission level.
        granted_by: Who granted permission.
        expires_at: Expiration timestamp.
    """

    user_id: str
    report_pattern: str
    level: PermissionLevel = PermissionLevel.READ
    granted_by: str = ""
    expires_at: Optional[float] = None
