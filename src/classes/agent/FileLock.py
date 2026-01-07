#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .LockType import LockType

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
class FileLock:
    """File lock information.

    Attributes:
        file_path: Path to the locked file.
        lock_type: Type of lock.
        owner: Lock owner identifier.
        acquired_at: Timestamp when lock was acquired.
        expires_at: Timestamp when lock expires (optional).
    """
    file_path: Path
    lock_type: LockType
    owner: str
    acquired_at: float
    expires_at: Optional[float] = None
