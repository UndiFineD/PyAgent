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

@dataclass
class ValidationRule:
    """A custom validation rule.

    Attributes:
        name: Rule name.
        file_pattern: Glob pattern for files to apply to.
        validator: Validation function.
        error_message: Message on validation failure.
        severity: Rule severity (error, warning, info).
    """

    name: str
    file_pattern: str
    validator: Callable[[str, Path], bool]
    error_message: str = "Validation failed"
    severity: str = "error"
