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

"""Context-lineage transaction manager with recursion guard.

Tracks active context IDs and a per-task stack using :mod:`contextvars`
so that concurrent asyncio tasks each get their own isolated state.
"""

from __future__ import annotations

import uuid
from contextvars import ContextVar, Token
from types import TracebackType
from typing import Any, List, Optional, Set

_active_var: ContextVar[Optional[Set[str]]] = ContextVar("_active_ctx", default=None)
_stack_var: ContextVar[Optional[List["ContextTransaction"]]] = ContextVar("_context_stack", default=None)


class RecursionGuardError(RuntimeError):
    """Raised when the same context_id is entered while already active."""


class ContextTransaction:
    """Track context lineage and prevent recursive re-entry of the same context.

    Attributes
    ----------
    context_id    : str       — caller-supplied logical name for this context.
    transaction_id: uuid.UUID — unique UUID assigned automatically.
    parent_id     : Optional[uuid.UUID] — transaction_id of the outer context, or None.

    """

    def __init__(
        self,
        context_id: str,
        *,
        parent_id: Optional[uuid.UUID] = None,
        tid: Optional[uuid.UUID] = None,
    ) -> None:
        """Initialize the transaction with a context_id
        and optional parent_id and tid.
        """
        if not context_id:
            raise ValueError("context_id must be a non-empty string")
        self.context_id: str = context_id
        self.transaction_id: uuid.UUID = tid if isinstance(tid, uuid.UUID) else uuid.uuid4()
        self.parent_id: Optional[uuid.UUID] = parent_id
        self._active_token: Optional[Token[Optional[Set[str]]]] = None
        self._stack_token: Optional[Token[Optional[List["ContextTransaction"]]]] = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_active() -> Set[str]:
        """Return the set of currently active context_id strings for this task."""
        v = _active_var.get()
        return v if v is not None else set()

    @staticmethod
    def _get_stack() -> List["ContextTransaction"]:
        """Return the current stack of active ContextTransaction objects for this task."""
        v = _stack_var.get()
        return v if v is not None else []

    # ------------------------------------------------------------------
    # Sync context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "ContextTransaction":
        """Enter the context manager, adding this transaction
        to the active set and stack.
        """
        active = self._get_active()
        if self.context_id in active:
            raise RecursionGuardError(f"Context {self.context_id!r} is already active (recursion guard).")
        stack = self._get_stack()
        # Inherit parent_id from the current stack head
        if stack:
            self.parent_id = stack[-1].transaction_id
        new_active = set(active) | {self.context_id}
        new_stack = list(stack) + [self]
        # Use tokens so __exit__ can restore the exact previous state
        self._active_token = _active_var.set(new_active)
        self._stack_token = _stack_var.set(new_stack)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the sync context manager, restoring ContextVar state."""
        # Restore ContextVar state to what it was before __enter__
        if self._active_token is not None:
            _active_var.reset(self._active_token)
            self._active_token = None
        if self._stack_token is not None:
            _stack_var.reset(self._stack_token)
            self._stack_token = None

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "ContextTransaction":
        """Enter the async context manager."""
        return self.__enter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the async context manager."""
        self.__exit__(exc_type, exc, tb)

    # ------------------------------------------------------------------
    # Class-level introspection
    # ------------------------------------------------------------------

    @classmethod
    def active_contexts(cls) -> Set[str]:
        """Return the set of currently active context_id strings."""
        v = _active_var.get()
        return v if v is not None else set()

    @classmethod
    def current(cls) -> Optional["ContextTransaction"]:
        """Return the innermost active ContextTransaction, or None."""
        stack = _stack_var.get()
        if stack:
            return stack[-1]
        return None

    # ------------------------------------------------------------------
    # Transaction protocol
    # ------------------------------------------------------------------

    async def commit(self) -> None:
        """No-op for ContextTransaction (lineage-only, no data to commit)."""

    async def rollback(self) -> None:
        """No-op for ContextTransaction."""

    async def hand_to_llm(self, context_window: Any) -> None:
        """Push a lineage summary into *context_window* for LLM consumption."""
        summary = (
            f"[ContextTransaction] id={self.transaction_id} context_id={self.context_id!r} parent_id={self.parent_id}"
        )
        if hasattr(context_window, "push"):
            context_window.push("system", summary)


def validate() -> bool:
    """Module-level health check."""
    return True
