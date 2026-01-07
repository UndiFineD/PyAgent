#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .SLALevel import SLALevel

from base_agent import BaseAgent
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

@dataclass
class SLAConfiguration:
    """SLA configuration for improvements.

    Attributes:
        level: SLA priority level.
        max_hours: Maximum hours to resolution.
        escalation_hours: Hours before escalation.
        notification_emails: Emails to notify.
    """
    level: SLALevel
    max_hours: int
    escalation_hours: int
    notification_emails: List[str] = field(default_factory=list)  # type: ignore[assignment]
