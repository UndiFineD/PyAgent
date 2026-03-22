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

"""Context-lineage transaction: prevents recursive re-entry for the same context ID."""

from __future__ import annotations

import threading
from types import TracebackType
from typing import Optional


def validate() -> bool:
    """Return True when ContextTransaction contracts are available."""
    return True


class RecursionGuardError(RuntimeError):
    """Raised when the same context_id is entered recursively."""


class ContextTransaction:
    """Guard against recursive re-entry for logically identical task contexts.

    Usage (sync)::

        with ContextTransaction("task-uuid") as ctx:
            ...  # "task-uuid" is in ContextTransaction.active_contexts()

    Usage (async)::

        async with ContextTransaction("task-uuid") as ctx:
            ...

    Entering the same *context_id* while it is already active raises
    :class:`RecursionGuardError`.  Passing an empty string raises
    :class:`ValueError`.
    """

    # Thread-local set of currently active context IDs.
    _local: threading.local = threading.local()

    def __init__(self, context_id: str) -> None:
        """Initialise the transaction with a non-empty context ID."""
        if not context_id:
            raise ValueError("context_id must not be empty.")
        self._context_id = context_id

    # ------------------------------------------------------------------
    # Class-level helpers
    # ------------------------------------------------------------------

    @classmethod
    def _active(cls) -> set[str]:
        """Return (and lazily initialise) the thread-local active-context set."""
        if not hasattr(cls._local, "contexts"):
            cls._local.contexts: set[str] = set()
        return cls._local.contexts

    @classmethod
    def active_contexts(cls) -> set[str]:
        """Return a *copy* of the currently active context IDs for this thread."""
        return set(cls._active())

    # ------------------------------------------------------------------
    # Internal enter / exit helpers
    # ------------------------------------------------------------------

    def _enter(self) -> "ContextTransaction":
        """Enter the transaction, adding the context ID to the active set."""
        active = self._active()
        if self._context_id in active:
            raise RecursionGuardError(
                f"Recursive re-entry detected for context id '{self._context_id}'."
            )
        active.add(self._context_id)
        return self

    def _exit(self, exc_type: Optional[type[BaseException]]) -> None:
        self._active().discard(self._context_id)

    # ------------------------------------------------------------------
    # Sync context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "ContextTransaction":
        """Enter the transaction, adding the context ID to the active set."""
        return self._enter()

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """Exit the transaction, removing the context ID from the active set.
        Return False to propagate exceptions."""
        self._exit(exc_type)
        return False

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "ContextTransaction":
        """Enter the transaction, adding the context ID to the active set."""
        return self._enter()

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """Exit the transaction, removing the context ID from the active set."""
        self._exit(exc_type)
        return False
