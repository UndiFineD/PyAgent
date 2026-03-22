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

"""Atomic file-system write transaction: stage → commit or rollback."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from types import TracebackType
from typing import Optional


def validate() -> bool:
    """Return True when StorageTransaction contracts are available."""
    return True


class StorageTransaction:
    """Atomic write transaction for a single target file.

    Usage (sync)::

        with StorageTransaction(path) as tx:
            tx.stage(b"content")
            tx.commit()   # optional: auto-commits on clean exit

    Usage (async)::

        async with StorageTransaction(path) as tx:
            tx.stage(b"content")

    On normal exit the staged content is written atomically via a temp-file
    rename.  On exception the target file is left untouched.
    """

    def __init__(self, target: Path) -> None:
        """Initialize transaction for *target* file."""
        self._target = Path(target)
        self._staged: Optional[bytes] = None
        self._committed = False
        self._rolled_back = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def stage(self, content: bytes) -> None:
        """Stage *content* to be written on commit."""
        self._staged = content

    def commit(self) -> None:
        """Write staged content to target atomically (tmp-file + rename)."""
        if self._committed or self._rolled_back:
            return
        if self._staged is None:
            return
        target = self._target
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=target.parent, prefix=".tx-")
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(self._staged)
            os.replace(tmp_path, target)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
        self._committed = True

    def rollback(self) -> None:
        """Discard staged content; target file is left unchanged."""
        self._staged = None
        self._rolled_back = True

    # ------------------------------------------------------------------
    # Sync context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "StorageTransaction":
        """Enter context: return self for staging/committing/rolling back."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """On normal exit commit staged content; on exception rollback (discard)."""
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        return False  # do not suppress exceptions

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "StorageTransaction":
        """Enter async context: return self for staging/committing/rolling back."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """On normal async exit commit staged content; on exception rollback."""
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        return False
