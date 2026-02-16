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

import pytest
from infrastructure.storage.memory.gpu_memory_allocator import MemoryState, AllocationStrategy, MemoryRegion, MemorySnapshot, MemoryPoolConfig, MemoryPressureEvent, CuMemAllocator, MultiGPUMemoryBalancer


def test_memorystate_basic():
    assert MemoryState is not None


def test_allocationstrategy_basic():
    assert AllocationStrategy is not None


def test_memoryregion_basic():
    assert MemoryRegion is not None


def test_memorysnapshot_basic():
    assert MemorySnapshot is not None


def test_memorypoolconfig_basic():
    assert MemoryPoolConfig is not None


def test_memorypressureevent_basic():
    assert MemoryPressureEvent is not None


def test_cumemallocator_basic():
    assert CuMemAllocator is not None


def test_multigpumemorybalancer_basic():
    assert MultiGPUMemoryBalancer is not None
