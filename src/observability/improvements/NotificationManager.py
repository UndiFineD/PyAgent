#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


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
