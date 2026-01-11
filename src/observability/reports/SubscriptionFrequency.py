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

class SubscriptionFrequency(Enum):
    """Frequency for report subscriptions."""

    IMMEDIATE = "immediate"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
