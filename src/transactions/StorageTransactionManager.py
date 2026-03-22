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

"""Atomic file-write transaction manager.

Supports two modes:
  - Legacy mode  : StorageTransaction(target: Path) — single-file atomic write.
  - Multi-op mode: StorageTransaction()            — async multi-op queue.
"""
from __future__ import annotations

import base64
import os
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple


class CommitError(RuntimeError):
    """Raised when commit() is called more than once on a committed transaction."""


class EncryptionConfigError(ValueError):
    """Raised when encryption is requested but PYAGENT_STORAGE_MASTER_KEY is absent."""


# ---------------------------------------------------------------------------
# Internal awaitable no-op helper (for await-compatible sync rollback)
# ---------------------------------------------------------------------------

async def _noop_coro() -> None:  # pragma: no cover
    pass


# ---------------------------------------------------------------------------
# StorageTransaction
# ---------------------------------------------------------------------------

class StorageTransaction:
    """Atomic file-write transaction.

    Legacy mode (target supplied)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Provides sync + async context-manager protocol over a single target file.
    Use ``stage(bytes)`` to buffer content, then ``commit()`` to write atomically
    (write to tmp → rename).  ``__exit__``/``__aexit__`` auto-commit on clean
    exit and rollback on exception.

    Multi-op mode (no target)
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    Provides an async queue of write/delete/mkdir operations executed together
    via ``acommit()``.  Optional per-write encryption via HKDF + Fernet when
    *user_id* is supplied (requires ``PYAGENT_STORAGE_MASTER_KEY`` env var).
    """

    def __init__(self, target: Optional[Path] = None) -> None:
        """Initialize the transaction with an optional target file (legacy mode)."""
        self._target: Optional[Path] = target
        self._staged: Optional[bytes] = None
        self._committed: bool = False
        self._tmp_path: Optional[Path] = None
        # Multi-op queue: list of ("write"|"delete"|"mkdir", path, optional_bytes)
        self._ops: List[Tuple[str, Path, Optional[bytes]]] = []

    # ------------------------------------------------------------------
    # Legacy-mode sync protocol
    # ------------------------------------------------------------------

    def stage(self, content: bytes) -> None:
        """Buffer *content* for atomic write on commit."""
        self._staged = content

    def commit(self) -> None:
        """Write staged content to target atomically (tmp-file + rename).

        Raises ``CommitError`` if called a second time after a successful commit.
        Is a safe no-op if nothing has been staged.
        """
        if self._staged is None:
            return  # no-op: nothing staged
        if self._committed:
            raise CommitError("Transaction already committed; cannot commit twice.")
        target = self._target
        if target is None:
            raise RuntimeError("commit() is only valid in legacy (single-file) mode.")
        # Write to a sibling tmp file then rename for atomicity
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=".tx_")
        self._tmp_path = Path(tmp)
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(self._staged)
            self._tmp_path.replace(target)
            self._tmp_path = None
        except Exception:
            try:
                Path(tmp).unlink(missing_ok=True)
            except OSError:
                pass
            raise
        self._committed = True

    def rollback(self):
        """Discard staged content and remove any tmp file.

        Safe to call in both sync and async contexts — returns an awaitable
        no-op coroutine so ``await tx.rollback()`` also works.
        """
        self._staged = None
        self._ops.clear()
        if self._tmp_path is not None:
            try:
                self._tmp_path.unlink(missing_ok=True)
            except OSError:
                pass
            self._tmp_path = None
        return _noop_coro()

    # ------------------------------------------------------------------
    # Sync context manager (legacy mode)
    # ------------------------------------------------------------------

    def __enter__(self) -> "StorageTransaction":
        """In legacy mode, simply return self.
        In multi-op mode, also allow nesting"""
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Exit the sync context manager."""
        if exc_type is not None:
            # Rollback: discard staged content and any tmp file
            self._staged = None
            if self._tmp_path is not None:
                try:
                    self._tmp_path.unlink(missing_ok=True)
                except OSError:
                    pass
                self._tmp_path = None
        elif self._target is not None and not self._committed and self._staged is not None:
            # Auto-commit on clean exit if content was staged
            self.commit()

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "StorageTransaction":
        """Enter the async context manager."""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Exit the async context manager.
        Behaves the same as sync __exit__
        (auto-commit on clean exit, rollback on exception)."""
        if exc_type is not None:
            # Rollback
            self._staged = None
            self._ops.clear()
            if self._tmp_path is not None:
                try:
                    self._tmp_path.unlink(missing_ok=True)
                except OSError:
                    pass
                self._tmp_path = None
        elif self._target is not None and not self._committed and self._staged is not None:
            # Legacy mode auto-commit on clean async exit
            self.commit()
        # Multi-op mode: no auto-commit; user must call acommit() explicitly

    # ------------------------------------------------------------------
    # Multi-op async protocol
    # ------------------------------------------------------------------

    async def write(self, path: Path, content: bytes, *, user_id: Optional[str] = None) -> None:
        """Queue a write operation.

        If *user_id* is provided, the content is encrypted with a key derived
        via HKDF-SHA256 from ``PYAGENT_STORAGE_MASTER_KEY`` env var.  Raises
        ``EncryptionConfigError`` when the env var is absent.
        """
        if user_id is not None:
            content = self._encrypt(content, user_id)
        self._ops.append(("write", Path(path), content))

    async def delete(self, path: Path) -> None:
        """Queue a delete operation."""
        self._ops.append(("delete", Path(path), None))

    async def mkdir(self, path: Path) -> None:
        """Queue a mkdir operation (creates all parents)."""
        self._ops.append(("mkdir", Path(path), None))

    async def acommit(self) -> None:
        """Execute all queued operations in order."""
        for op, path, content in list(self._ops):
            if op == "write":
                path.parent.mkdir(parents=True, exist_ok=True)
                fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tx_")
                tmp_path = Path(tmp)
                try:
                    with os.fdopen(fd, "wb") as fh:
                        fh.write(content)  # type: ignore[arg-type]
                    tmp_path.replace(path)
                except Exception:
                    try:
                        tmp_path.unlink(missing_ok=True)
                    except OSError:
                        pass
                    raise
            elif op == "delete":
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
            elif op == "mkdir":
                path.mkdir(parents=True, exist_ok=True)
        self._ops.clear()

    # ------------------------------------------------------------------
    # Encryption helper
    # ------------------------------------------------------------------

    def _encrypt(self, content: bytes, user_id: str) -> bytes:
        """Derive a Fernet key via HKDF and encrypt *content*.

        Raises ``EncryptionConfigError`` if ``PYAGENT_STORAGE_MASTER_KEY``
        is not set in the environment.
        """
        master_key_b64 = os.environ.get("PYAGENT_STORAGE_MASTER_KEY")
        if not master_key_b64:
            raise EncryptionConfigError(
                "PYAGENT_STORAGE_MASTER_KEY environment variable is required for encrypted writes."
            )
        try:
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.hkdf import HKDF
            from cryptography.fernet import Fernet
        except ImportError as exc:
            raise EncryptionConfigError("cryptography package is required for encrypted writes.") from exc

        master_key = base64.b64decode(master_key_b64)
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=user_id.encode(),
            info=b"storage-tx",
        )
        derived = hkdf.derive(master_key)
        fernet_key = base64.urlsafe_b64encode(derived)
        f = Fernet(fernet_key)
        return f.encrypt(content)


def validate() -> bool:
    """Module-level health check."""
    return True
