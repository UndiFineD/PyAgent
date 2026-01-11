#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from src.core.base.utils._helpers import _empty_dict_str_any

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
class ScheduledExecution:
    """A scheduled agent execution.

    Attributes:
        name: Schedule name.
        cron: Cron expression (simplified).
        agent_config: Agent configuration.
        enabled: Whether schedule is enabled.
        last_run: Last run timestamp.
        next_run: Next run timestamp.
    """

    name: str
    cron: str  # Simplified: "hourly", "daily", "weekly", or HH:MM
    agent_config: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    enabled: bool = True
    last_run: Optional[float] = None
    next_run: Optional[float] = None
