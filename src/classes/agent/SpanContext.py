#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .TelemetrySpan import TelemetrySpan

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

class SpanContext:
    """Context for a telemetry span."""

    def __init__(self, span: TelemetrySpan) -> None:
        """Initialize context.

        Args:
            span: The span to manage.
        """
        self._span = span

    def set_attribute(self, key: str, value: Any) -> None:
        """Set a span attribute.

        Args:
            key: Attribute key.
            value: Attribute value.
        """
        self._span.attributes[key] = value

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add an event to the span.

        Args:
            name: Event name.
            attributes: Event attributes.
        """
        self._span.events.append({
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {},
        })
