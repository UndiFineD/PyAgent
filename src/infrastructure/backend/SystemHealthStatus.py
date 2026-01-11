#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .SystemState import SystemState

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
class SystemHealthStatus:
    """Health status for a backend.

    Attributes:
        backend: Backend identifier.
        state: Current health state.
        last_check: Last health check timestamp.
        success_rate: Success rate (0.0 - 1.0).
        avg_latency_ms: Average latency.
        error_count: Recent error count.
    """

    backend: str
    state: SystemState
    last_check: float = field(default_factory=time.time)
    success_rate: float = 1.0
    avg_latency_ms: float = 0.0
    error_count: int = 0
