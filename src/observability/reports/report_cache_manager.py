#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Report Cache Manager - Manage report caching with TTL-based invalidation

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Instantiate ReportCacheManager(cache_file=Path("...")) then call .get(file_path, content_hash) to retrieve a cached report, .set(file_path, content_hash, content, ttl=...) to store a report, and .invalidate(file_path) or .invalidate() to remove entries.

WHAT IT DOES:
- Persists a simple cache mapping of "file_path:content_hash" -> {"content": str, "expires_at": epoch}
- Loads/saves the cache to a JSON file (default .report_cache.json under src/)
- Provides TTL-based expiration checks and invalidation by file path or full clear
- Logs warnings on load/save failures and tolerates JSON or IO errors

WHAT IT SHOULD DO BETTER:
- Add atomic file writes and file locking to avoid corruption and race conditions when multiple processes/threads access the cache.
- Enforce size limits, eviction strategy (LRU), and background cleanup of expired entries to avoid unbounded cache growth.
- Normalize and validate keys/paths and improve error reporting (raise explicit exceptions or surface failures rather than only logging).
- Support richer metadata (creation time, last-access) and configurable persistence format, and add unit tests for edge cases and concurrent access.

FILE CONTENT SUMMARY:
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

# Define AGENT_DIR for default parameter

AGENT_DIR = Path(__file__).resolve().parent.parent.parent  # src/


class ReportCacheManager:
    """Manages report caching with invalidation strategies.
    Attributes:
        cache_file: Path to cache file.
        _cache: Current cache data mapping (path, hash) -> (content, ttl_end).
    """

    def __init__(self, cache_file: Path | None = None) -> None:
        """Initialize cache manager.
        Args:
            cache_file: Path to cache file. Defaults to .report_cache.json.
        """

        self.cache_file = cache_file or AGENT_DIR / ".report_cache.json"
        self._cache: dict[str, Any] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        """Load cache from disk."""

        if self.cache_file.exists():
            try:
                data = json.loads(self.cache_file.read_text())
                self._cache = data.get("cache", {})
            except (IOError, OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
                logging.warning(f"Failed to load cache: {e}")

    def _save_cache(self) -> None:
        """Save cache to disk."""

        try:
            data: dict[str, Any] = {"cache": self._cache}
            self.cache_file.write_text(json.dumps(data, indent=2))
        except (IOError, OSError, TypeError, UnicodeEncodeError) as e:
            logging.warning(f"Failed to save cache: {e}")

    def get(self, file_path: str, content_hash: str) -> str | None:
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
        if time.time() > entry.get("expires_at", 0):
            return None
        return entry.get("content")

    def set(self, file_path: str, content_hash: str, content: str, ttl: int = 3600) -> None:
        """Cache report content.
        Args:
            file_path: Path to source file.
            content_hash: Content hash.
            content: Report content to cache.
            ttl: Time-to-live in seconds.
        """

        cache_key = f"{file_path}:{content_hash}"
        self._cache[cache_key] = {"content": content, "expires_at": time.time() + ttl}
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

    def invalidate(self, file_path: str | None = None) -> None:
        """Invalidate cache entries.
        Args:
            file_path: Path to invalidate. If None, clears all.
        """

        if file_path:
            self.invalidate_by_path(file_path)
        else:
            self._cache.clear()
            self._save_cache()
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

# Define AGENT_DIR for default parameter

AGENT_DIR = Path(__file__).resolve().parent.parent.parent  # src/


class ReportCacheManager:
    """Manages report caching with invalidation strategies.
    Attributes:
        cache_file: Path to cache file.
        _cache: Current cache data mapping (path, hash) -> (content, ttl_end).
    """

    def __init__(self, cache_file: Path | None = None) -> None:
        """Initialize cache manager.
        Args:
            cache_file: Path to cache file. Defaults to .report_cache.json.
        """

        self.cache_file = cache_file or AGENT_DIR / ".report_cache.json"
        self._cache: dict[str, Any] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        """Load cache from disk."""

        if self.cache_file.exists():
            try:
                data = json.loads(self.cache_file.read_text())
                self._cache = data.get("cache", {})
            except (IOError, OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
                logging.warning(f"Failed to load cache: {e}")

    def _save_cache(self) -> None:
        """Save cache to disk."""

        try:
            data: dict[str, Any] = {"cache": self._cache}
            self.cache_file.write_text(json.dumps(data, indent=2))
        except (IOError, OSError, TypeError, UnicodeEncodeError) as e:
            logging.warning(f"Failed to save cache: {e}")

    def get(self, file_path: str, content_hash: str) -> str | None:
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
        if time.time() > entry.get("expires_at", 0):
            return None
        return entry.get("content")

    def set(self, file_path: str, content_hash: str, content: str, ttl: int = 3600) -> None:
        """Cache report content.
        Args:
            file_path: Path to source file.
            content_hash: Content hash.
            content: Report content to cache.
            ttl: Time-to-live in seconds.
        """

        cache_key = f"{file_path}:{content_hash}"
        self._cache[cache_key] = {"content": content, "expires_at": time.time() + ttl}
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

    def invalidate(self, file_path: str | None = None) -> None:
        """Invalidate cache entries.
        Args:
            file_path: Path to invalidate. If None, clears all.
        """

        if file_path:
            self.invalidate_by_path(file_path)
        else:
            self._cache.clear()
            self._save_cache()
