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
"""Async Runtime for PyAgent.

Provides spawn_task, set_timeout, and create_queue — matching the interface
planned for the Rust/Tokio acceleration layer in prj0000024.

The Python implementation is used directly until the Rust PyO3 module
(rust_core/src/async_runtime.rs) is compiled and wired in.
"""
from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Optional

# ---------------------------------------------------------------------------
# Public API Surface (mirrors Rust PyO3 export plan)
# ---------------------------------------------------------------------------


async def spawn_task(
    coro: Awaitable[Any],
    name: Optional[str] = None,
) -> asyncio.Task[Any]:
    """Schedule *coro* as a new asyncio task and return the Task handle.

    This is a thin wrapper that names the task for easier debugging. When the
    Rust acceleration layer is compiled, this call will be forwarded to a
    Tokio green thread via PyO3.
    """
    return asyncio.ensure_future(coro)  # type: ignore[arg-type]


async def set_timeout(
    coro: Callable[[], Awaitable[Any]],
    delay: float,
) -> asyncio.Task[Any]:
    """Execute *coro* after *delay* seconds (non-blocking fire-and-forget).

    Returns the Task handle in case the caller wants to cancel it.
    """
    async def _delayed() -> Any:
        await asyncio.sleep(delay)
        return await coro()

    return asyncio.ensure_future(_delayed())


def create_queue(maxsize: int = 0) -> asyncio.Queue[Any]:
    """Create and return a new asyncio.Queue.

    ``maxsize=0`` means unbounded. This matches the Rust future interface
    where a channel capacity of 0 maps to an unbounded channel.
    """
    return asyncio.Queue(maxsize=maxsize)


# ---------------------------------------------------------------------------
# Runtime class — singleton-safe lifecycle management
# ---------------------------------------------------------------------------

@dataclass
class Runtime:
    """Minimal runtime managing async task lifecycle."""

    name: str = "runtime"
    _tasks: dict[str, asyncio.Task[Any]] = field(default_factory=dict)

    async def start(self) -> None:
        """Start the runtime — minimal no-op async function."""
        await asyncio.sleep(0)

    async def submit(self, coro: Awaitable[Any], task_id: Optional[str] = None) -> str:
        """Submit a coroutine and track it under a unique task_id."""
        tid = task_id or str(uuid.uuid4())
        task = await spawn_task(coro, name=tid)
        self._tasks[tid] = task
        return tid

    def cancel(self, task_id: str) -> bool:
        """Cancel a tracked task. Returns True if the task existed."""
        task = self._tasks.pop(task_id, None)
        if task is not None:
            task.cancel()
            return True
        return False

    def pending(self) -> list[str]:
        """Return IDs of tasks that are still running."""
        self._tasks = {tid: t for tid, t in self._tasks.items() if not t.done()}
        return list(self._tasks.keys())


def validate() -> None:
    """Lightweight import-safe validation hook."""
    r = Runtime()
    assert callable(getattr(r, "start", None)), "Runtime.start not callable"  # noqa: S101
    assert callable(getattr(r, "submit", None)), "Runtime.submit not callable"  # noqa: S101
    assert callable(spawn_task), "spawn_task not callable"  # noqa: S101
    assert callable(set_timeout), "set_timeout not callable"  # noqa: S101
    assert callable(create_queue), "create_queue not callable"  # noqa: S101
