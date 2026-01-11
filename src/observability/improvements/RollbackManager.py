#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .RollbackPoint import RollbackPoint

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

class RollbackManager:
    """Stores rollback points and can restore the latest state."""

    def __init__(self) -> None:
        self.rollbacks: List[RollbackPoint] = []
        self._by_id: Dict[str, List[RollbackPoint]] = {}

    def create_rollback_point(self, improvement_id: str, state: Dict[str, Any]) -> RollbackPoint:
        point = RollbackPoint(improvement_id=improvement_id, state=dict(state))
        self.rollbacks.append(point)
        self._by_id.setdefault(improvement_id, []).append(point)
        return point

    def rollback(self, improvement_id: str) -> Dict[str, Any]:
        points = self._by_id.get(improvement_id, [])
        if not points:
            return {}
        point = points[-1]
        return dict(point.state)
