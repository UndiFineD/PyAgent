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
"""Tests for src.core.task_queue."""

import asyncio
import importlib


async def _producer_consumer_cycle() -> None:
    """Test that we can enqueue and dequeue items from the TaskQueue."""
    import src.core.task_queue as tq

    q = tq.TaskQueue()

    # put an item and get it back
    await q.put("x")
    item = await q.get()
    assert item == "x"


def test_task_queue_validate_and_async_cycle() -> None:
    """Test that the task_queue module can be imported and validate function runs."""
    tq = importlib.import_module("src.core.task_queue")
    assert hasattr(tq, "TaskQueue"), "TaskQueue missing"
    assert callable(getattr(tq, "validate", None)), "validate missing"

    # run simple async producer/consumer
    asyncio.run(_producer_consumer_cycle())


def test_task_queue_validate_executes() -> None:
    """validate() must exercise both hasattr checks in its body."""
    from src.core.task_queue import validate

    # invoking validate() should not raise — covers lines 48-49
    validate()


def test_task_queue_module() -> None:
    """Test that the task_queue module can be imported and has expected components."""
    qmod = importlib.import_module("src.core.task_queue")
    assert hasattr(qmod, "TaskQueue")
    assert callable(getattr(qmod, "validate", None))
