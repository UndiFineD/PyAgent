#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .BackendType import BackendType

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
class BackendConfig:
    """Configuration for a single backend.

    Attributes:
        name: Backend identifier.
        backend_type: Type of backend.
        enabled: Whether backend is active.
        weight: Weight for load balancing.
        timeout_s: Request timeout in seconds.
        max_retries: Maximum retry attempts.
        rate_limit_rpm: Requests per minute limit.
    """

    name: str
    backend_type: BackendType
    enabled: bool = True
    weight: int = 1
    timeout_s: int = 60
    max_retries: int = 2
    rate_limit_rpm: Optional[int] = None
