#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

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

class AccessController:
    """Tracks per-improvement permissions and roles."""

    def __init__(self) -> None:
        self.permissions: Dict[str, Dict[str, set[str]]] = {}
        self._roles: Dict[str, List[str]] = {}
        self._assigned_roles: Dict[str, Dict[str, str]] = {}

    def define_role(self, role: str, permissions: List[str]) -> None:
        self._roles[role] = list(permissions)

    def assign_role(self, improvement_id: str, user: str, role: str) -> None:
        self._assigned_roles.setdefault(improvement_id, {})[user] = role

    def grant(self, improvement_id: str, user: str, level: str) -> None:
        self.permissions.setdefault(improvement_id, {}).setdefault(user, set()).add(level)

    def can_access(self, improvement_id: str, user: str, level: str) -> bool:
        direct = level in self.permissions.get(improvement_id, {}).get(user, set())
        if direct:
            return True
        role = self._assigned_roles.get(improvement_id, {}).get(user)
        if role and role in self._roles:
            return level in self._roles[role]
        return False
