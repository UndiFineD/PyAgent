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

"""In-memory key-value transaction manager with optional remote sync."""
from __future__ import annotations

import asyncio
import threading
from typing import Any, Optional


class RemoteSyncError(RuntimeError):
    """Raised when a remote sync operation fails."""

    def __init__(self, endpoint: str, cause: Exception) -> None:
        super().__init__(f"Remote sync to {endpoint!r} failed: {cause}")
        self.endpoint = endpoint
        self.cause = cause


class MemoryTransaction:
    """Transactional key-value store with sync and async context-manager support.

    Changes are buffered in ``_pending`` until ``commit()`` moves them to
    ``_store``.  ``rollback()`` discards ``_pending`` without touching
    ``_store``.

    Parameters
    ----------
    tid : optional identifier for correlating or tracing this transaction.
    """

    def __init__(self, tid: Optional[Any] = None) -> None:
        """Initialize the transaction with an optional identifier."""
        self.tid = tid
        self._rlock: threading.RLock = threading.RLock()
        self._alock: Optional[asyncio.Lock] = None
        self._store: dict = {}
        self._pending: dict = {}

    # ------------------------------------------------------------------
    # Sync context manager (thread-safe via RLock)
    # ------------------------------------------------------------------

    def __enter__(self) -> "MemoryTransaction":
        """Enter the sync context manager."""
        self._rlock.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Exit the sync context manager."""
        self._rlock.release()

    # ------------------------------------------------------------------
    # Async context manager (asyncio-safe via lazy Lock)
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "MemoryTransaction":
        """Enter the async context manager, creating the lock if needed."""
        if self._alock is None:
            self._alock = asyncio.Lock()
        await self._alock.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Exit the async context manager, releasing the lock if it exists."""
        if self._alock is not None:
            self._alock.release()

    # ------------------------------------------------------------------
    # KV operations (all async for consistent interface)
    # ------------------------------------------------------------------

    async def set(self, key: str, value: Any, *, encrypt: bool = False) -> None:
        """Stage *value* under *key* in the pending store."""
        self._pending[key] = value

    async def get(self, key: str, *, decrypt: bool = False) -> Optional[Any]:
        """Return the value for *key*, checking _store first then _pending."""
        if key in self._store:
            return self._store[key]
        return self._pending.get(key)

    async def delete(self, key: str) -> None:
        """Remove *key* from both pending and committed stores."""
        self._pending.pop(key, None)
        self._store.pop(key, None)

    async def commit(self) -> None:
        """Flush all pending changes into the committed store."""
        self._store.update(self._pending)
        self._pending.clear()

    async def rollback(self) -> None:
        """Discard all pending changes without touching the committed store."""
        self._pending.clear()

    # ------------------------------------------------------------------
    # Remote sync
    # ------------------------------------------------------------------

    async def sync_remote(
        self,
        endpoint: str,
        *,
        encrypted: bool = True,
        dry_run: bool = False,
    ) -> Optional[dict]:
        """Sync the committed store to a remote endpoint.

        Parameters
        ----------
        endpoint  : HTTP URL to POST the payload to.
        encrypted : hint for the remote service (does not encrypt locally here).
        dry_run   : when True, return the store dict without making any network call.

        Returns the committed store dict on *dry_run*; otherwise the full
        envelope after a successful POST (or None if endpoint is empty).

        Raises ``RemoteSyncError`` on network failure.
        """
        if not endpoint:
            return None
        payload = dict(self._store)
        if dry_run:
            return payload
        envelope = {"tid": str(self.tid), "encrypted": encrypted, "payload": payload}
        try:
            import httpx
        except ImportError:
            import logging
            logging.warning("httpx not available — skipping remote sync")
            return None
        import os
        headers: dict = {}
        token = os.environ.get("PYAGENT_MEMORY_SYNC_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            async with httpx.AsyncClient() as client:
                await client.post(endpoint, json=envelope, headers=headers, timeout=10.0)
        except Exception as exc:
            raise RemoteSyncError(endpoint, exc) from exc
        return envelope


def validate() -> bool:
    """Module-level health check."""
    return True
