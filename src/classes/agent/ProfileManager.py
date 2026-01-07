#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .ExecutionProfile import ExecutionProfile

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

class ProfileManager:
    """Manage agent execution profiles.

    Example:
        manager=ProfileManager()
        manager.add_profile(ExecutionProfile("ci", dry_run=True, timeout=60))
        manager.add_profile(ExecutionProfile("full", parallel=True, workers=8))

        manager.activate("ci")
        config=manager.get_active_config()
    """

    def __init__(self) -> None:
        """Initialize manager."""
        self._profiles: Dict[str, ExecutionProfile] = {}
        self._active: Optional[str] = None
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default profiles."""
        self._profiles["default"] = ExecutionProfile(
            name="default",
            timeout=120,
            parallel=False,
        )

        self._profiles["fast"] = ExecutionProfile(
            name="fast",
            max_files=10,
            timeout=60,
            parallel=True,
            workers=4,
        )

        self._profiles["ci"] = ExecutionProfile(
            name="ci",
            timeout=300,
            parallel=True,
            workers=2,
            dry_run=True,
        )

    def add_profile(self, profile: ExecutionProfile) -> None:
        """Add a profile.

        Args:
            profile: Profile to add.
        """
        self._profiles[profile.name] = profile

    def activate(self, name: str) -> None:
        """Activate a profile.

        Args:
            name: Profile name.

        Raises:
            KeyError: If profile not found.
        """
        if name not in self._profiles:
            raise KeyError(f"Profile not found: {name}")
        self._active = name

    def get_active_config(self) -> Optional[ExecutionProfile]:
        """Get active profile configuration."""
        if self._active:
            return self._profiles[self._active]
        return None
