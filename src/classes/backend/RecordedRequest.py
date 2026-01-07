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
class RecordedRequest:
    """A recorded request for replay."""

    request_id: str
    timestamp: float
    prompt: str
    backend: str
    response: Optional[str] = None
    latency_ms: int = 0
    success: bool = True
    metadata: Dict[str, Any] = field(default_factory=lambda: {})
