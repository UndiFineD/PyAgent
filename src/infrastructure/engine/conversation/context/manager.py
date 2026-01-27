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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Context manager for coordinating multiple conversation contexts.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional, Type, TypeVar

from .core import AgenticContext, ConversationContext
from .models import ContextConfig, ContextSnapshot, ContextState

T = TypeVar("T", bound=ConversationContext)
logger = logging.getLogger(__name__)


class ContextManager:
    """
    Registry and lifecycle manager for conversation contexts.
    """

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, default_config: Optional[ContextConfig] = None) -> None:
=======
    def __init__(self, default_config: Optional[ContextConfig] = None):
<<<<<<< HEAD
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
    def __init__(self, default_config: Optional[ContextConfig] = None) -> None:
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
=======
    def __init__(self, default_config: Optional[ContextConfig] = None) -> None:
>>>>>>> 797ca81d4 (Fix Pylint errors: imports, whitespace, docstrings)
        """Initialize the context manager."""
        self._contexts: Dict[str, ConversationContext] = {}
        self._default_config = default_config or ContextConfig()
        self._cleanup_task: Optional[asyncio.Task] = None
        self._is_running = False

    @property
    def active_contexts_count(self) -> int:
        """Get the number of active contexts."""
        return len([c for c in self._contexts.values() if c.is_active])

    def create_context(
        self,
        context_id: Optional[str] = None,
        config: Optional[ContextConfig] = None,
        context_class: Type[T] = AgenticContext,
        **kwargs: Any,
    ) -> T:
        """Create and register a new context."""
        cfg = config or self._default_config
        ctx = context_class(context_id=context_id, config=cfg, **kwargs)

        if ctx.context_id in self._contexts:
            raise ValueError(f"Context ID {ctx.context_id} already exists")

        self._contexts[ctx.context_id] = ctx
        logger.info(f"Created context: {ctx.context_id}")
        return ctx

    def get_context(self, context_id: str) -> Optional[ConversationContext]:
        """Retrieve a context by ID."""
        return self._contexts.get(context_id)

    def remove_context(self, context_id: str) -> bool:
        """Remove and cleanup a context."""
        ctx = self._contexts.pop(context_id, None)
        if ctx:
            logger.info(f"Removed context: {context_id}")
            return True
        return False

    async def start_background_cleanup(self, interval: int = 300) -> None:
        """Start background task to purge expired contexts."""
        if self._cleanup_task and not self._cleanup_task.done():
            return

        self._is_running = True
        self._cleanup_task = asyncio.create_task(self._cleanup_loop(interval))

    async def stop_background_cleanup(self) -> None:
        """Stop maintenance task."""
        self._is_running = False
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

    async def _cleanup_loop(self, interval: int) -> None:
        """Maintenance loop."""
        while self._is_running:
            try:
                await asyncio.sleep(interval)
                await self.purge_expired_contexts()
            except asyncio.CancelledError:
                break
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.error(f"Error in context cleanup: {e}")

    async def purge_expired_contexts(self) -> int:
        """Remove contexts that have exceeded their TTL."""
        expired_ids = []
        now = time.time()

        for ctx_id, ctx in self._contexts.items():
            ttl = ctx.config.ttl
            if 0 < ttl < (now - ctx.last_activity):
                expired_ids.append(ctx_id)

        count = 0
        for ctx_id in expired_ids:
            ctx = self._contexts[ctx_id]
            await ctx.cleanup()
            self.remove_context(ctx_id)
            count += 1

        if count > 0:
            logger.info(f"Purged {count} expired contexts")

        return count

    def list_contexts(self, state: Optional[ContextState] = None) -> List[str]:
        """List context IDs, optionally filtered by state."""
        if state is None:
            return list(self._contexts.keys())
        return [cid for cid, ctx in self._contexts.items() if ctx.state == state]

    async def shutdown(self) -> None:
        """Gracefully shut down all contexts."""
        await self.stop_background_cleanup()
        ids = list(self._contexts.keys())
        for cid in ids:
            ctx = self._contexts[cid]
            await ctx.cleanup()
            self.remove_context(cid)
        logger.info("Context Manager shut down")


# Storage for global context manager instance
_MANAGER_STORAGE: Dict[str, Optional[ContextManager]] = {"instance": None}


def get_context_manager() -> ContextManager:
    """Get or create singleton instance."""
    if _MANAGER_STORAGE["instance"] is None:
        _MANAGER_STORAGE["instance"] = ContextManager()
    return _MANAGER_STORAGE["instance"]


def create_context(
    context_id: Optional[str] = None,
    config: Optional[ContextConfig] = None,
    context_class: Type[ConversationContext] = AgenticContext,
    **kwargs: Any,
) -> ConversationContext:
    """Convenience function to create a context using the global manager."""
    return get_context_manager().create_context(
        context_id=context_id, config=config, context_class=context_class, **kwargs
    )


def merge_contexts(
    primary: ConversationContext, secondary: ConversationContext, deduplicate: bool = True
) -> ConversationContext:
    """Merge turns from secondary into primary context."""
    primary.import_turns(secondary.turns, deduplicate=deduplicate)
    return primary


def restore_context(snapshot: ContextSnapshot) -> ConversationContext:
    """Restore context from a snapshot."""
    return ConversationContext.from_snapshot(snapshot)
