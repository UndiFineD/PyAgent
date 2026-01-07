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
class QueuedRequest:
    """A request waiting in the queue.

    Attributes:
        priority: Request priority (higher=more urgent).
        timestamp: When request was queued.
        request_id: Unique request identifier.
        prompt: The prompt to send.
        callback: Optional callback function.
    """

    priority: int
    timestamp: float
    request_id: str
    prompt: str
    callback: Optional[Callable[[str], None]] = None

    def __lt__(self, other: "QueuedRequest") -> bool:
        """Compare by priority (descending) then timestamp (ascending)."""
        if self.priority != other.priority:
            return self.priority > other.priority  # Higher priority first
        return self.timestamp < other.timestamp  # Earlier first
