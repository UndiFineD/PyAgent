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
"""Tests for TaskScheduler (prj0000022)."""

import pytest

from swarm.task_scheduler import TaskScheduler


@pytest.mark.asyncio
async def test_enqueue_and_dequeue():
    sched = TaskScheduler()
    tid = sched.enqueue({"action": "run"}, priority=2)
    task = await sched.dequeue()
    assert task["id"] == tid
    assert task["payload"]["action"] == "run"


@pytest.mark.asyncio
async def test_priority_ordering():
    sched = TaskScheduler()
    sched.enqueue({"a": 1}, priority=4)
    tid_high = sched.enqueue({"b": 2}, priority=1)
    first = await sched.dequeue()
    assert first["id"] == tid_high


@pytest.mark.asyncio
async def test_dequeue_empty_raises():
    sched = TaskScheduler()
    with pytest.raises(IndexError):
        await sched.dequeue()


def test_modify_priority():
    sched = TaskScheduler()
    tid = sched.enqueue({"x": 1}, priority=3)
    sched.modify(tid, priority=1)
    assert sched._tasks[tid]["priority"] == 1
