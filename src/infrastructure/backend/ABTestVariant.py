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
class ABTestVariant:
    """A variant in an A / B test."""

    name: str
    backend: str
    weight: float = 0.5
    metrics: Dict[str, float] = field(default_factory=lambda: {})
    sample_count: int = 0
