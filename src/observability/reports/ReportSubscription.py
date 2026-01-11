#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from generate_agent_reports.py"""

from .ReportType import ReportType
from .SubscriptionFrequency import SubscriptionFrequency

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
class ReportSubscription:
    """Subscription for report delivery.
    Attributes:
        subscriber_id: Unique subscriber identifier.
        email: Email address for delivery.
        frequency: Delivery frequency.
        report_types: Types of reports to receive.
        file_patterns: Patterns for files to include.
        enabled: Whether subscription is active.
    """

    subscriber_id: str
    email: str
    frequency: SubscriptionFrequency = SubscriptionFrequency.DAILY
    report_types: List[ReportType] = field(default_factory=list)  # type: ignore[assignment]
    file_patterns: List[str] = field(default_factory=list)  # type: ignore[assignment]
    enabled: bool = True
