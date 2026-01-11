#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

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

class AssignmentManager:
    """Tracks assignees and ownership history."""

    def __init__(self) -> None:
        self.assignments: Dict[str, str] = {}
        self._history: Dict[str, List[Dict[str, Any]]] = {}

    def assign(self, improvement_id: str, assignee: str) -> None:
        self.assignments[improvement_id] = assignee
        self._history.setdefault(improvement_id, []).append(
            {"assignee": assignee, "timestamp": datetime.now().isoformat()}
        )

    def get_assignee(self, improvement_id: str) -> Optional[str]:
        return self.assignments.get(improvement_id)

    def get_ownership_history(self, improvement_id: str) -> List[Dict[str, Any]]:
        return list(self._history.get(improvement_id, []))
