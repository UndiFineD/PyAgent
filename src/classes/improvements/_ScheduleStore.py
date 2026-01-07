#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .ScheduledImprovement import ScheduledImprovement

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

class _ScheduleStore:
    """Mapping wrapper that compares equal to {} and [] when empty."""

    def __init__(self) -> None:
        self._data: Dict[str, ScheduledImprovement] = {}

    def __eq__(self, other: object) -> bool:
        if isinstance(other, dict):
            return self._data == other
        if isinstance(other, list):
            return len(other) == 0 and len(self._data) == 0
        return False

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __getitem__(self, key: str) -> ScheduledImprovement:
        return self._data[key]

    def __setitem__(self, key: str, value: ScheduledImprovement) -> None:
        self._data[key] = value

    def get(self, key: str, default: Optional[ScheduledImprovement] = None) -> Optional[ScheduledImprovement]:
        return self._data.get(key, default)

    def values(self) -> List[ScheduledImprovement]:
        return list(self._data.values())
