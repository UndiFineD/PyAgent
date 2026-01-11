#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .Improvement import Improvement
from .TransitionResult import TransitionResult

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

class WorkflowEngine:
    """Manages improvement workflow transitions."""

    def __init__(self) -> None:
        self.states: List[str] = [
            "pending",
            "in_progress",
            "completed",
            "blocked",
        ]
        self._transitions: Dict[str, List[str]] = {
            "pending": ["in_progress", "blocked"],
            "in_progress": ["completed", "blocked"],
            "blocked": ["in_progress"],
            "completed": [],
        }

    def transition(self, improvement: Improvement, from_status: str, to_status: str) -> TransitionResult:
        allowed = self._transitions.get(from_status, [])
        if to_status not in allowed:
            return TransitionResult(success=False, message="Invalid transition")

        # Tests expect string status updates.
        setattr(improvement, "status", to_status)
        return TransitionResult(success=True)
