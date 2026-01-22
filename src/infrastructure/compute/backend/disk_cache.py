"""
Disk-based cache for persistent storage.
(Facade for src.core.base.common.cache_core)
"""

from src.core.base.common.cache_core import CacheCore as StandardCacheCore

<<<<<<< HEAD
<<<<<<< HEAD
"""Disk-based cache for persistent storage."""

from __future__ import annotations
from src.core.base.version import VERSION
import json
import logging
import time
from pathlib import Path
from typing import Optional

__version__ = VERSION

class DiskCache:
    """A simple disk-based cache for persistent storage of AI responses."""
=======
class DiskCache(StandardCacheCore):
    """Facade for CacheCore."""
    pass
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
class DiskCache(StandardCacheCore):
    """Facade for CacheCore."""
    pass
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    def __init__(self, cache_dir: Path, ttl_seconds: float | None = None) -> None:
        """Initialize disk cache.

        Args:
            cache_dir: Directory where cache files will be stored.
            ttl_seconds: Optional time-to-live for cache entries.
        """
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_seconds
        self._ensure_cache_dir()

    def _ensure_cache_dir(self) -> None:
        """Ensure the cache directory exists."""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create cache directory {self.cache_dir}: {e}")

    def _get_file_path(self, key: str) -> Path:
        """Generate a file path for a cache key."""
        return self.cache_dir / f"{key}.json"

    def set(self, key: str, value: str) -> None:
        """Set a cache entry.

        Args:
            key: Cache key (should be a hash).
            value: Value to cache.
        """
        file_path = self._get_file_path(key)
        data = {
            "key": key,
            "value": value,
            "timestamp": time.time()
        }
        try:
            file_path.write_text(json.dumps(data), encoding="utf-8")
        except Exception as e:
            logging.warning(f"Failed to write cache file {file_path}: {e}")

    def get(self, key: str) -> str | None:
        """Get a cache entry.

        Args:
            key: Cache key.

        Returns:
            The cached value, or None if not found or expired.
        """
        file_path = self._get_file_path(key)
        if not file_path.exists():
            return None

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            
            # Check TTL
            if self.ttl_seconds is not None:
                timestamp = data.get("timestamp", 0)
                if time.time() - timestamp > self.ttl_seconds:
                    logging.debug(f"Cache entry {key} expired")
                    try:
                        file_path.unlink()
                    except Exception:
                        logging.debug(f"Failed to unlink expired cache file {file_path}")
                    return None
            
            return data.get("value")
        except Exception as e:
            logging.warning(f"Failed to read cache file {file_path}: {e}")
            return None

    def clear(self) -> None:
        """Clear all cache entries."""
        try:
            for file_path in self.cache_dir.glob("*.json"):
                file_path.unlink()
            logging.debug(f"Cleared disk cache at {self.cache_dir}")
        except Exception as e:
            logging.error(f"Failed to clear disk cache: {e}")