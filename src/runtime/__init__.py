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

"""Compatibility shim for the ``runtime`` module used by tests.

When the compiled Rust extension is not installed, tests import this module
from ``src/runtime``. We provide the same minimal API surface expected by the
suite: ``spawn_task``, ``set_timeout``, ``create_queue``, and
``_shutdown_runtime``.
"""

from __future__ import annotations

import asyncio
import inspect
from collections.abc import Awaitable, Callable
from typing import Any


def spawn_task(py_coro: Awaitable[Any]) -> None:
    """Schedule a coroutine on the active asyncio event loop."""
    try:
        asyncio.create_task(py_coro)
    except Exception:
        # Avoid leaving the coroutine un-awaited and emitting warnings.
        if inspect.iscoroutine(py_coro):
            py_coro.close()  # type: ignore[attr-defined]
        raise


def set_timeout(ms: float, callback: Callable[[], None]) -> None:
    """Execute *callback* after *ms* milliseconds."""
    loop = asyncio.get_event_loop()
    loop.call_later(ms / 1000.0, callback)


def create_queue() -> tuple[asyncio.Queue[Any], Callable[[Any], Awaitable[None]]]:
    """Return an asyncio queue and its ``put`` coroutine method."""
    queue: asyncio.Queue[Any] = asyncio.Queue()
    return queue, queue.put


def _shutdown_runtime() -> None:
    """No-op shutdown hook for API compatibility."""
    return None
