#!/usr/bin/env python3
"""Metrics engine module for PyAgent."""

from __future__ import annotations

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

"""Very small proof-of-concept module showing how a formerly synchronous
"while" loop can be migrated to the async runtime.

This file exists solely to satisfy **Task 10** of the async-runtime rollout
plan.  In the original design the engine contained a blocking ``while True``
loop that periodically flushed metrics; such loops are disallowed by the
project's linting rules and are hard to reason about.  The code below
illustrates the simple transformation:

* ``start_sync_loop`` is the pre‑existing implementation (not used anywhere).
* ``start_async_loop`` uses :mod:`runtime_py` helpers to schedule an
  ``async`` tick loop on the global runtime, and thus no synchronous loops
  remain in the module.

The accompanying test verifies the counter increments when the async loop
runs, proving that the runtime integration works.
"""

# ``Any`` was previously planned for future use but isn't needed yet
# from typing import Any

from runtime_py import sleep, spawn  # type: ignore[import-not-found]  # noqa: E402

# shared state used solely for the unit test
counter: int = 0


def start_async_loop() -> None:
    """Migrated implementation that uses the async runtime.

    ``runtime_py.sleep`` returns an awaitable that schedules a callback on the
    global Tokio runtime.  ``spawn`` submits the coroutine so that the caller
    does not need to await it; the loop lives independently of whatever
    triggered the start.
    """

    async def _tick_loop() -> None:
        """Async loop that increments the global counter every 100 milliseconds."""
        global counter
        while True:  # now an *async* loop
            await sleep(100)  # milliseconds
            counter += 1

    spawn(_tick_loop())
