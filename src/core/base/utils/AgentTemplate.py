#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from src.core.base.utils._helpers import _empty_dict_str_any, _empty_list_str

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
class AgentTemplate:
    """A template for creating agents.

    Attributes:
        name: Template name.
        description: Template description.
        agents: List of agents to execute.
        config: Default configuration.
        file_patterns: File patterns to process.
    """

    name: str
    description: str = ""
    agents: list[str] = field(default_factory=_empty_list_str)
    config: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    file_patterns: list[str] = field(default_factory=lambda: ["*.py"])
