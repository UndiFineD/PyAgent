#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .AgentPriority import AgentPriority
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
class AgentPluginConfig:
    """Configuration for an agent plugin.

    Attributes:
        name: Unique plugin name.
        module_path: Path to the plugin module.
        entry_point: Entry point function name.
        priority: Execution priority.
        enabled: Whether the plugin is enabled.
        config: Plugin - specific configuration.
    """
    name: str
    module_path: str
    entry_point: str = "run"
    priority: AgentPriority = AgentPriority.NORMAL
    enabled: bool = True
    config: dict[str, Any] = field(default_factory=_empty_dict_str_any)
