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
class ReportTemplate:
    """Template for report generation.
    Attributes:
        name: Template name.
        sections: List of section names to include.
        include_metadata: Whether to include metadata section.
        include_summary: Whether to include summary section.
    """

    name: str
    sections: List[str] = field(
        default_factory=lambda: ["purpose", "location", "surface"]
    )  # type: ignore[assignment]
    include_metadata: bool = True
    include_summary: bool = True
