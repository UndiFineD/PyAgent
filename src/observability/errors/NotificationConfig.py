#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_errors.py"""

from .ErrorSeverity import ErrorSeverity
from .NotificationChannel import NotificationChannel

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class NotificationConfig:
    """Configuration for error notifications.

    Attributes:
        channel: Notification channel type.
        endpoint: Webhook URL or email address.
        min_severity: Minimum severity to notify.
        enabled: Whether notifications are enabled.
        template: Message template.
    """
    channel: NotificationChannel
    endpoint: str
    min_severity: ErrorSeverity = ErrorSeverity.HIGH
    enabled: bool = True
    template: str = "Error: {message} in {file}:{line}"
