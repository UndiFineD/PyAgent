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

"""Context lineage transaction manager.

:class:`ContextTransaction` maintains a thread-local / task-local stack
of active context identifiers.  When a context ID is entered a second
time before it is exited, a :class:`RecursionGuardError` is raised to
prevent infinite recursion in swarm workflows.

Both synchronous and asynchronous ``with`` blocks are supported.
"""

from __future__ import annotations

import threading
from typing import Any, Optional, Type


class RecursionGuardError(RuntimeError):
    """Raised when a context ID is entered recursively."""


# Thread-local storage for the active context stack.
_local = threading.local()


def _active_stack() -> list[str]:
    """Return the active context stack for the current thread."""
    if not hasattr(_local, "stack"):
        _local.stack = []
    return _local.stack  # type: ignore[return-value]


class ContextTransaction:
    """Guard against re-entrant execution of the same context ID.

    Parameters
    ----------
    context_id:
        Unique identifier for the task or operation being guarded.
        Must not be an empty string.
    tid:
        Optional opaque transaction identifier for tracing.

    Usage::

        with ContextTransaction("task-abc") as ctx:
            # safe to execute, context_id is on the active stack
            ...
        # context_id removed from stack after exit

        # Recursive entry raises RecursionGuardError:
        with ContextTransaction("task-abc"):
            with ContextTransaction("task-abc"):  # raises RecursionGuardError
                ...
    """

    def __init__(self, context_id: str, tid: Optional[Any] = None) -> None:
        if not context_id:
            raise ValueError("context_id must not be empty")
        self.context_id = context_id
        self.tid = tid

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _push(self) -> None:
        stack = _active_stack()
        if self.context_id in stack:
            raise RecursionGuardError(
                f"Context '{self.context_id}' is already active — recursive entry prevented"
            )
        stack.append(self.context_id)

    def _pop(self) -> None:
        stack = _active_stack()
        if self.context_id in stack:
            stack.remove(self.context_id)

    @staticmethod
    def active_contexts() -> list[str]:
        """Return a snapshot of the currently active context IDs."""
        return list(_active_stack())

    # ------------------------------------------------------------------
    # Sync context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "ContextTransaction":
        self._push()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[Any],
    ) -> None:
        self._pop()

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "ContextTransaction":
        self._push()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[Any],
    ) -> None:
        self._pop()
