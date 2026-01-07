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
class BackendCapability:
    """A capability supported by a backend."""

    name: str
    description: str
    enabled: bool = True
    parameters: Dict[str, Any] = field(default_factory=lambda: {})
