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
import base64
import json
import os
import threading
from pathlib import Path
from types import TracebackType
from typing import Any, Optional
from urllib.parse import urlparse

from src.core import security_bridge


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
        self._store: dict[str, Any] = {}
        self._pending: dict[str, Any] = {}

    def _memory_key_file(self) -> str:
        """Return key-file path used by in-memory encryption/decryption."""
        key_file = os.environ.get("PYAGENT_MEMORY_KEY_FILE")
        if not key_file:
            raise ValueError(
                "PYAGENT_MEMORY_KEY_FILE is required when encrypt/decrypt is enabled for MemoryTransaction."
            )
        return key_file

    @staticmethod
    def _pack_value(value: Any) -> str:
        """Serialize supported Python values into an encrypted payload string."""
        if isinstance(value, bytes):
            payload = {
                "type": "bytes",
                "value": base64.b64encode(value).decode("ascii"),
            }
            return json.dumps(payload)

        payload = {
            "type": "json",
            "value": value,
        }
        try:
            return json.dumps(payload)
        except TypeError as exc:
            raise TypeError("MemoryTransaction encryption supports JSON-serializable values and bytes.") from exc

    @staticmethod
    def _unpack_value(payload_text: str) -> Any:
        """Deserialize encrypted payload string back to the original Python value."""
        payload = json.loads(payload_text)
        payload_type = payload.get("type")
        if payload_type == "bytes":
            encoded = payload.get("value", "")
            return base64.b64decode(encoded)
        if payload_type == "json":
            return payload.get("value")
        raise ValueError(f"Unsupported encrypted payload type: {payload_type!r}")

    # ------------------------------------------------------------------
    # Sync context manager (thread-safe via RLock)
    # ------------------------------------------------------------------

    def __enter__(self) -> "MemoryTransaction":
        """Enter the sync context manager."""
        self._rlock.acquire()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
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

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the async context manager, releasing the lock if it exists."""
        if self._alock is not None:
            self._alock.release()

    # ------------------------------------------------------------------
    # KV operations (all async for consistent interface)
    # ------------------------------------------------------------------

    async def set(self, key: str, value: Any, *, encrypt: bool = False) -> None:
        """Stage *value* under *key* in the pending store."""
        if encrypt:
            key_file = self._memory_key_file()
            ciphertext = security_bridge.encrypt(Path(key_file), self._pack_value(value))
            self._pending[key] = {"__enc__": ciphertext}
            return
        self._pending[key] = value

    async def get(self, key: str, *, decrypt: bool = False) -> Optional[Any]:
        """Return the value for *key*, checking _store first then _pending."""
        if key in self._store:
            value = self._store[key]
        else:
            value = self._pending.get(key)

        if not decrypt or value is None:
            return value

        if isinstance(value, dict) and "__enc__" in value:
            key_file = self._memory_key_file()
            plaintext = security_bridge.decrypt(Path(key_file), str(value["__enc__"]))
            return self._unpack_value(plaintext)

        return value

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

    async def sync_remote(  # noqa: D417
        self,
        endpoint: str,
        *,
        encrypted: bool = True,
        dry_run: bool = False,
    ) -> Optional[dict[str, Any]]:
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
        parsed = urlparse(endpoint)
        if parsed.scheme not in ("https", "http"):
            raise ValueError(
                f"sync_remote: unsupported URL scheme {parsed.scheme!r}. Only 'https' and 'http' are accepted."
            )
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
        headers: dict[str, str] = {}
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
