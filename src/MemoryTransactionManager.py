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

"""Simple transaction helper for in-memory structures.

This module provides :class:`MemoryTransaction`, a context manager that
acquires a process-wide lock before yielding control.  The goal is to
ensure that any modifications to shared in-memory data structures are
performed atomically.  The current implementation is intentionally
lightweight; it only uses a reentrant thread lock and supports both
synchronous and asynchronous ``with`` blocks so callers can write the
same code regardless of the surrounding framework.

When a real storage layer is introduced the implementation can be
replaced with a more sophisticated transaction manager (WAL, write-ahead
log, etc.) without touching the clients.
"""

from __future__ import annotations

import threading
from typing import Optional, Type, Any

# global lock used by all transactions; reentrant so that nested
# transactions from the same thread do not deadlock.
_lock = threading.RLock()


class MemoryTransaction:
    """Context manager for a logical memory transaction.

    Acquire :data:`_lock` on enter and release it on exit.  Both synchronous
    and asynchronous protocol methods are provided so callers can use
    ``with`` or ``async with`` without needing to know which one they
    are in.

    ``tid`` is an opaque identifier that clients can supply when they
    wish to trace or correlate transactions; it is not used by the
    implementation today but kept for API compatibility with the design
    document.
    """

    def __init__(self, tid: Optional[Any] = None) -> None:
        """Initialize the transaction with an optional identifier."""
        self.tid = tid

    def __enter__(self) -> "MemoryTransaction":
        """Acquire the lock to begin the transaction."""
        _lock.acquire()
        return self

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Optional[Any]
    ) -> None:
        """Release the lock to end the transaction."""
        _lock.release()

    async def __aenter__(self) -> "MemoryTransaction":
        """Acquire the lock to begin the transaction."""
        _lock.acquire()
        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Optional[Any]
    ) -> None:
        """Release the lock to end the transaction."""
        _lock.release()
