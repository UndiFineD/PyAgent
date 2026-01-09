#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

class ConnectionPool:
    """
    Manages a pool of reusable connections with Phase 108 status caching.
    Reduces connection overhead and prevents repeated failure pings by
    caching 'working' status for 15 minutes.
    """

    def __init__(self, max_connections: int = 10, timeout_s: float = 30.0, cache_file: Optional[str] = None) -> None:
        """Initialize connection pool."""
        self.max_connections = max_connections
        self.timeout_s = timeout_s
        self._pools: Dict[str, List[Any]] = {}
        self._in_use: Dict[str, int] = {}
        self._lock = threading.Lock()
        
        # Phase 108: Status Caching (15 minute TTL)
        self.status_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = 900 # 15 minutes
        self.cache_file = Path(cache_file) if cache_file else None
        self._load_status_cache()

    def _load_status_cache(self) -> None:
        if self.cache_file and self.cache_file.exists():
            try:
                self.status_cache = json.loads(self.cache_file.read_text())
            except Exception:
                pass

    def _save_status_cache(self) -> None:
        if self.cache_file:
            try:
                self.cache_file.parent.mkdir(parents=True, exist_ok=True)
                self.cache_file.write_text(json.dumps(self.status_cache))
            except Exception:
                pass

    def is_backend_working(self, backend: str) -> bool:
        """Checks if the backend is cached as working within the last 15 minutes."""
        with self._lock:
            status = self.status_cache.get(backend)
            if status:
                elapsed = time.time() - status.get("timestamp", 0)
                if elapsed < self.cache_ttl:
                    return status.get("working", False)
        return True # Default to True if no cache or expired

    def set_backend_status(self, backend: str, working: bool) -> None:
        """Updates the working status of a backend."""
        with self._lock:
            self.status_cache[backend] = {
                "working": working,
                "timestamp": time.time()
            }
            self._save_status_cache()

    def acquire(self, backend: str) -> Any:
        """Acquire a connection, respecting the status cache (Phase 108)."""
        if not self.is_backend_working(backend):
            logging.debug(f"ConnectionPool: Skipping '{backend}' (cached as non-working)")
            return None

        with self._lock:
            if backend not in self._pools:
                self._pools[backend] = []
                self._in_use[backend] = 0

            pool = self._pools[backend]

            if pool:
                # Reuse existing connection
                conn = pool.pop()
                self._in_use[backend] += 1
                return conn

            if self._in_use[backend] < self.max_connections:
                # Create new connection
                conn = self._create_connection(backend)
                self._in_use[backend] += 1
                return conn

            # Pool exhausted
            logging.warning(f"Connection pool exhausted for {backend}")
            return None

    def release(self, backend: str, connection: Any) -> None:
        """Release connection back to pool.

        Args:
            backend: Backend identifier.
            connection: Connection to release.
        """
        with self._lock:
            if backend in self._pools:
                self._pools[backend].append(connection)
                self._in_use[backend] = max(0, self._in_use.get(backend, 1) - 1)

    def _create_connection(self, backend: str) -> Dict[str, Any]:
        """Create a new connection (placeholder).

        Args:
            backend: Backend identifier.

        Returns:
            Dict: Connection object placeholder.
        """
        return {
            "backend": backend,
            "created_at": time.time(),
            "id": str(uuid.uuid4()),
        }

    def get_stats(self) -> Dict[str, Dict[str, int]]:
        """Get pool statistics.

        Returns:
            Dict: Pool stats by backend.
        """
        with self._lock:
            return {
                backend: {
                    "available": len(pool),
                    "in_use": self._in_use.get(backend, 0),
                    "max": self.max_connections,
                }
                for backend, pool in self._pools.items()
            }

    def close_all(self) -> int:
        """Close all connections.

        Returns:
            int: Number of connections closed.
        """
        with self._lock:
            count = sum(len(pool) for pool in self._pools.values())
            self._pools.clear()
            self._in_use.clear()
        return count
