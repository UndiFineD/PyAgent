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
"""Tests for the async runtime module — prj0000024."""

import asyncio

import pytest

# ---------------------------------------------------------------------------
# Import tests
# ---------------------------------------------------------------------------


def test_core_runtime_module_importable():
    """core.runtime must be importable and expose the async API."""
    from src.core import runtime as r

    assert hasattr(r, "Runtime")
    assert hasattr(r, "spawn_task")
    assert hasattr(r, "set_timeout")
    assert hasattr(r, "create_queue")
    assert hasattr(r, "validate")


def test_validate_passes():
    from src.core.runtime import validate

    validate()  # must not raise


# ---------------------------------------------------------------------------
# spawn_task
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_spawn_task_runs_coro():
    from src.core.runtime import spawn_task

    result: list[int] = []

    async def work() -> None:
        result.append(42)

    task = await spawn_task(work())
    await task
    assert result == [42]


# ---------------------------------------------------------------------------
# set_timeout
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_set_timeout_fires():
    from src.core.runtime import set_timeout

    result: list[str] = []

    async def work() -> None:
        result.append("fired")

    await set_timeout(lambda: work(), delay=0.01)
    await asyncio.sleep(0.05)
    assert result == ["fired"]


# ---------------------------------------------------------------------------
# create_queue
# ---------------------------------------------------------------------------


def test_create_queue_unbounded():
    from src.core.runtime import create_queue

    q = create_queue(0)
    assert isinstance(q, asyncio.Queue)


@pytest.mark.asyncio
async def test_queue_put_get():
    from src.core.runtime import create_queue

    q = create_queue()
    await q.put("hello")
    val = await q.get()
    assert val == "hello"


# ---------------------------------------------------------------------------
# Runtime class
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_runtime_start():
    from src.core.runtime import Runtime

    rt = Runtime()
    await rt.start()


@pytest.mark.asyncio
async def test_runtime_submit_and_pending():
    from src.core.runtime import Runtime

    rt = Runtime()
    ran: list[int] = []

    async def noop() -> None:
        await asyncio.sleep(0)
        ran.append(1)

    tid = await rt.submit(noop())
    assert isinstance(tid, str)
    await asyncio.sleep(0.05)
    pending = rt.pending()
    assert tid not in pending


@pytest.mark.asyncio
async def test_runtime_cancel():
    from src.core.runtime import Runtime

    rt = Runtime()

    async def long_task() -> None:
        await asyncio.sleep(10)

    tid = await rt.submit(long_task())
    assert rt.cancel(tid) is True
    assert rt.cancel(tid) is False  # second cancel returns False (already removed)


# ---------------------------------------------------------------------------
# Legacy stub — keeps old test passing for other CI consumers
# ---------------------------------------------------------------------------


def test_runtime_stubs_present():
    """core.runtime exposes the expected stub functions."""
    from src.core import runtime

    assert hasattr(runtime, "spawn_task")
    assert hasattr(runtime, "set_timeout")
    assert hasattr(runtime, "create_queue")
