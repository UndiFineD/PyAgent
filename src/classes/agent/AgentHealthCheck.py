#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .HealthStatus import HealthStatus
from ._helpers import _empty_dict_str_any

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
class AgentHealthCheck:
    """Health check result for an agent.

    Attributes:
        agent_name: Name of the agent.
        status: Health status.
        response_time_ms: Response time in milliseconds.
        last_check: Timestamp of last health check.
        error_message: Error message if unhealthy.
        details: Additional health details.
    """
    agent_name: str
    status: HealthStatus
    response_time_ms: float = 0.0
    last_check: float = field(default_factory=time.time)
    error_message: Optional[str] = None
    details: dict[str, Any] = field(default_factory=_empty_dict_str_any)
