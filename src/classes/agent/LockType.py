#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

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

class LockType(Enum):
    """File locking type."""
    SHARED = auto()       # Multiple readers allowed
    EXCLUSIVE = auto()    # Single writer only
    ADVISORY = auto()     # Advisory lock (not enforced by OS)
