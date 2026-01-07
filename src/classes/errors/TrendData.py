#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from .TrendDirection import TrendDirection

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
class TrendData:
    """Error trend analysis data.

    Attributes:
        metric_name: Name of the metric being tracked.
        values: Historical values.
        timestamps: Timestamps for each value.
        direction: Current trend direction.
        prediction: Predicted next value.
    """
    metric_name: str
    values: List[float] = field(default_factory=lambda: [])
    timestamps: List[str] = field(default_factory=lambda: [])
    direction: TrendDirection = TrendDirection.STABLE
    prediction: Optional[float] = None
