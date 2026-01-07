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
class BackendResponse:
    """Response from a backend request.

    Attributes:
        content: Response content.
        backend: Backend that provided response.
        latency_ms: Response latency in milliseconds.
        cached: Whether response was from cache.
        request_id: ID of originating request.
        tokens_used: Estimated tokens consumed.
    """

    content: str
    backend: str
    latency_ms: int = 0
    cached: bool = False
    request_id: Optional[str] = None
    tokens_used: int = 0
