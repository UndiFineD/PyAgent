#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .CompletionTrend import CompletionTrend
from .Improvement import Improvement

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

class AnalyticsEngine:
    """Very small analytics engine used by tests."""

    def __init__(self) -> None:
        self._completed: List[Improvement] = []

    def record_completion(self, improvement: Improvement) -> None:
        self._completed.append(improvement)

    def get_completion_trend(self, period_days: int = 30) -> CompletionTrend:
        return CompletionTrend(total_completed=len(self._completed))

    def calculate_velocity(self, sprint_days: int = 14) -> float:
        total_points = 0.0
        for imp in self._completed:
            total_points += float(getattr(imp, "story_points", 0) or 0)
        return total_points / (float(sprint_days) / 7.0) if sprint_days else 0.0
