#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from ._helpers import _empty_dict_str_any, _empty_list_dict_str_any

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
class TelemetrySpan:
    """A telemetry span for tracing.

    Attributes:
        name: Span name.
        trace_id: Trace identifier.
        span_id: Span identifier.
        parent_id: Parent span ID.
        start_time: Start timestamp.
        end_time: End timestamp.
        attributes: Span attributes.
        events: Span events.
    """

    name: str
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    parent_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    attributes: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    events: list[dict[str, Any]] = field(default_factory=_empty_list_dict_str_any)
