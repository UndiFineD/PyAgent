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

"""Atomic file-system transaction manager.

:class:`StorageTransaction` writes to a temporary file alongside the
target path and atomically replaces the target on commit using
:func:`os.replace`.  On rollback (or if the context exits with an
exception) the temporary file is removed without touching the target.

Both synchronous and asynchronous ``with`` blocks are supported so
callers can use the same API regardless of their surrounding framework.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any, Optional, Type


class StorageTransaction:
    """Write-then-atomically-replace file transaction.

    Parameters
    ----------
    target:
        Destination path that will receive the content on commit.
    tid:
        Optional opaque transaction identifier for tracing.

    Usage::

        with StorageTransaction("config.json") as tx:
            tx.stage(b'{"key": "value"}')
        # file now exists at config.json

        # rollback example:
        with StorageTransaction("config.json") as tx:
            tx.stage(b"bad data")
            raise ValueError("oops")   # triggers rollback, target untouched
    """

    def __init__(self, target: str | Path, tid: Optional[Any] = None) -> None:
        self.target = Path(target)
        self.tid = tid
        self._tmp_path: Optional[Path] = None
        self._committed = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def stage(self, data: bytes) -> None:
        """Write *data* to the temporary staging file.

        May be called multiple times; each call replaces the previous
        staged content.
        """
        if self._tmp_path is None:
            raise RuntimeError("StorageTransaction not entered — use as a context manager")
        self._tmp_path.write_bytes(data)

    def commit(self) -> None:
        """Atomically move the staged file to the target path."""
        if self._tmp_path is None or not self._tmp_path.exists():
            raise RuntimeError("Nothing staged; call stage() before commit()")
        self.target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(self._tmp_path, self.target)
        self._tmp_path = None
        self._committed = True

    def rollback(self) -> None:
        """Discard the staged file without touching the target."""
        if self._tmp_path is not None and self._tmp_path.exists():
            self._tmp_path.unlink(missing_ok=True)
        self._tmp_path = None

    # ------------------------------------------------------------------
    # Sync context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "StorageTransaction":
        fd, tmp = tempfile.mkstemp(
            prefix=".stx_", dir=self.target.parent if self.target.parent.exists() else None
        )
        os.close(fd)
        self._tmp_path = Path(tmp)
        self._committed = False
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[Any],
    ) -> None:
        if exc_type is None and not self._committed:
            # auto-commit if no exception was raised and caller did not
            # explicitly call commit/rollback
            try:
                self.commit()
            except RuntimeError:
                pass  # nothing was staged — that's fine
        else:
            self.rollback()

    # ------------------------------------------------------------------
    # Async context manager (delegates to sync logic)
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "StorageTransaction":
        return self.__enter__()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[Any],
    ) -> None:
        self.__exit__(exc_type, exc, tb)
