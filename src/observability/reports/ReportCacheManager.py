#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from generate_agent_reports.py"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

# Define AGENT_DIR for default parameter

































from src.core.base.version import VERSION
__version__ = VERSION

AGENT_DIR = Path(__file__).resolve().parent.parent.parent  # src/

class ReportCacheManager:
    """Manages report caching with invalidation strategies.
    Attributes:
        cache_file: Path to cache file.
        _cache: Current cache data mapping (path, hash) -> (content, ttl_end).
    """

    def __init__(self, cache_file: Optional[Path] = None) -> None:
        """Initialize cache manager.
        Args:
            cache_file: Path to cache file. Defaults to .report_cache.json.
        """

        self.cache_file = cache_file or AGENT_DIR / ".report_cache.json"
        self._cache: Dict[str, Any] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        """Load cache from disk."""

        if self.cache_file.exists():
            try:
                data = json.loads(self.cache_file.read_text())
                self._cache = data.get('cache', {})
            except Exception as e:
                logging.warning(f"Failed to load cache: {e}")

    def _save_cache(self) -> None:
        """Save cache to disk."""

        try:
            data: Dict[str, Any] = {
                'cache': self._cache
            }
            self.cache_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logging.warning(f"Failed to save cache: {e}")

    def get(self, file_path: str, content_hash: str) -> Optional[str]:
        """Get cached report if valid.
        Args:
            file_path: Path to source file.
            content_hash: Current content hash.
        Returns:
            Cached content or None if not valid or expired.
        """

        cache_key = f"{file_path}:{content_hash}"
        if cache_key not in self._cache:
            return None
        entry = self._cache[cache_key]
        # Check if expired
        if time.time() > entry.get('expires_at', 0):
            return None
        return entry.get('content')

    def set(self, file_path: str, content_hash: str, content: str, ttl: int = 3600) -> None:
        """Cache report content.
        Args:
            file_path: Path to source file.
            content_hash: Content hash.
            content: Report content to cache.
            ttl: Time-to-live in seconds.
        """

        cache_key = f"{file_path}:{content_hash}"
        self._cache[cache_key] = {
            'content': content,
            'expires_at': time.time() + ttl
        }
        self._save_cache()

    def invalidate_by_path(self, file_path: str) -> None:
        """Invalidate all cache entries for a file path.
        Args:
            file_path: Path to file.
        """

        keys_to_delete = [k for k in self._cache.keys() if k.startswith(f"{file_path}:")]
        for key in keys_to_delete:
            del self._cache[key]
        self._save_cache()

    def invalidate(self, file_path: Optional[str] = None) -> None:
        """Invalidate cache entries.
        Args:
            file_path: Path to invalidate. If None, clears all.
        """

        if file_path:
            self.invalidate_by_path(file_path)
        else:
            self._cache.clear()
            self._save_cache()
