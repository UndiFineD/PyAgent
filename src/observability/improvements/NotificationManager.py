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

class NotificationManager:
    """Notifies subscribers about improvement changes."""

    def __init__(self) -> None:
        self.subscribers: List[str] = []
        self._subscriptions: Dict[str, List[str]] = {}
        self._callbacks: List[Callable[[Dict[str, Any]], None]] = []

    def subscribe(self, improvement_id: str, subscriber: str) -> None:
        self.subscribers.append(subscriber)
        self._subscriptions.setdefault(improvement_id, []).append(subscriber)

    def get_subscribers(self, improvement_id: str) -> List[str]:
        return list(self._subscriptions.get(improvement_id, []))

    def on_notification(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        self._callbacks.append(callback)

    def notify_status_change(self, improvement_id: str, old_status: str, new_status: str) -> None:
        payload = {
            "improvement_id": improvement_id,
            "old_status": old_status,
            "new_status": new_status,
        }
        for cb in list(self._callbacks):
            cb(payload)
