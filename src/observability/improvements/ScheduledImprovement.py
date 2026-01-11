#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .ScheduleStatus import ScheduleStatus

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class ScheduledImprovement:
    """A scheduled improvement with resource allocation.

    Attributes:
        improvement_id: ID of the scheduled improvement.
        scheduled_start: Planned start date.
        scheduled_end: Planned end date.
        assigned_resources: List of assigned team members.
        status: Current schedule status.
        sprint_id: Optional sprint identifier.
    """
    improvement_id: str
    scheduled_start: str = ""
    scheduled_end: str = ""
    assigned_resources: List[str] = field(default_factory=list)  # type: ignore[assignment]
    status: ScheduleStatus = ScheduleStatus.UNSCHEDULED
    sprint_id: str = ""
