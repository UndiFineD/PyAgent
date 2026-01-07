#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .RateLimitStrategy import RateLimitStrategy

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting.

    Attributes:
        requests_per_second: Maximum requests per second.
        requests_per_minute: Maximum requests per minute.
        burst_size: Maximum burst size for token bucket.
        strategy: Rate limiting strategy to use.
        cooldown_seconds: Cooldown period after hitting limit.
    """
    requests_per_second: float = 10.0
    requests_per_minute: int = 60
    burst_size: int = 10
    strategy: RateLimitStrategy = RateLimitStrategy.TOKEN_BUCKET
    cooldown_seconds: float = 1.0
