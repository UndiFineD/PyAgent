#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .CachedResult import CachedResult

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

class ResultCache:
    """Cache agent results for reuse.

    Example:
        cache=ResultCache()

        # Check cache
        result=cache.get("test.py", "coder", content_hash)
        if result is None:
            result=run_coder("test.py")
            cache.set("test.py", "coder", content_hash, result)
    """

    def __init__(self, cache_dir: Optional[Path] = None) -> None:
        """Initialize cache.

        Args:
            cache_dir: Directory for persistent cache.
        """
        self.cache_dir = cache_dir
        self._memory_cache: Dict[str, CachedResult] = {}

    def _make_key(self, file_path: str, agent_name: str, content_hash: str) -> str:
        """Create cache key."""
        return f"{file_path}:{agent_name}:{content_hash}"

    def get(
        self,
        file_path: str,
        agent_name: str,
        content_hash: str,
    ) -> Optional[Any]:
        """Get cached result.

        Args:
            file_path: File path.
            agent_name: Agent name.
            content_hash: Hash of content.

        Returns:
            Cached result or None.
        """
        key = self._make_key(file_path, agent_name, content_hash)

        if key in self._memory_cache:
            cached = self._memory_cache[key]
            # Check TTL
            if time.time() - cached.timestamp < cached.ttl_seconds:
                return cached.result
            else:
                del self._memory_cache[key]

        return None

    def set(
        self,
        file_path: str,
        agent_name: str,
        content_hash: str,
        result: Any,
        ttl_seconds: int = 3600,
    ) -> None:
        """Cache a result.

        Args:
            file_path: File path.
            agent_name: Agent name.
            content_hash: Hash of content.
            result: Result to cache.
            ttl_seconds: Time to live.
        """
        key = self._make_key(file_path, agent_name, content_hash)
        self._memory_cache[key] = CachedResult(
            file_path=file_path,
            agent_name=agent_name,
            content_hash=content_hash,
            result=result,
            ttl_seconds=ttl_seconds,
        )

    def invalidate(self, file_path: str) -> int:
        """Invalidate all cache entries for a file.

        Args:
            file_path: File path.

        Returns:
            Number of entries invalidated.
        """
        to_remove = [k for k in self._memory_cache if k.startswith(f"{file_path}:")]
        for key in to_remove:
            del self._memory_cache[key]
        return len(to_remove)

    def clear(self) -> None:
        """Clear all cached results."""
        self._memory_cache.clear()
