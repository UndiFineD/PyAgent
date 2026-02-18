#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import pytest
except ImportError:
    import pytest

try:
    from core.base.logic.structures.lock_free_queue import QueueStats, MPMCQueue, SPSCQueue, PriorityItem, PriorityQueue, WorkStealingDeque, BatchingQueue
except ImportError:
    from core.base.logic.structures.lock_free_queue import QueueStats, MPMCQueue, SPSCQueue, PriorityItem, PriorityQueue, WorkStealingDeque, BatchingQueue



def test_queuestats_basic():
    assert QueueStats is not None


def test_mpmcqueue_basic():
    assert MPMCQueue is not None


def test_spscqueue_basic():
    assert SPSCQueue is not None


def test_priorityitem_basic():
    assert PriorityItem is not None


def test_priorityqueue_basic():
    assert PriorityQueue is not None


def test_workstealingdeque_basic():
    assert WorkStealingDeque is not None


def test_batchingqueue_basic():
    assert BatchingQueue is not None
