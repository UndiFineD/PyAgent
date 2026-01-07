#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from ._helpers import _empty_list_str

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
class ShutdownState:
    """State for graceful shutdown.

    Attributes:
        shutdown_requested: Whether shutdown has been requested.
        current_file: Currently processing file.
        completed_files: List of completed files.
        pending_files: List of pending files.
        start_time: Processing start time.
    """
    shutdown_requested: bool = False
    current_file: Optional[str] = None
    completed_files: list[str] = field(default_factory=_empty_list_str)
    pending_files: list[str] = field(default_factory=_empty_list_str)
    start_time: float = field(default_factory=time.time)
