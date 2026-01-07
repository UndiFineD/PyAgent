#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from ._helpers import _empty_dict_str_float, _empty_dict_str_str, _empty_list_str

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
class IncrementalState:
    """State for incremental processing.

    Attributes:
        last_run_timestamp: Timestamp of last successful run.
        processed_files: Dict of file paths to their last processed timestamp.
        file_hashes: Dict of file paths to their content hashes.
        pending_files: List of files pending processing.
    """
    last_run_timestamp: float = 0.0
    processed_files: dict[str, float] = field(default_factory=_empty_dict_str_float)
    file_hashes: dict[str, str] = field(default_factory=_empty_dict_str_str)
    pending_files: list[str] = field(default_factory=_empty_list_str)
