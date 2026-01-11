#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

@dataclass
class UsageQuota:
    """Usage quota configuration.

    Attributes:
        daily_limit: Maximum requests per day.
        hourly_limit: Maximum requests per hour.
        current_daily: Current daily usage.
        current_hourly: Current hourly usage.
        reset_daily_at: When daily count resets.
        reset_hourly_at: When hourly count resets.
    """

    daily_limit: int = 1000
    hourly_limit: int = 100
    current_daily: int = 0
    current_hourly: int = 0
    reset_daily_at: float = field(default_factory=time.time)
    reset_hourly_at: float = field(default_factory=time.time)
