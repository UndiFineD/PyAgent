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
import time
from src.infrastructure.engine.workspace.workspace_manager import WorkspaceManager
from src.infrastructure.engine.workspace.ubatching_utils import UBatchingUtils
from src.infrastructure.engine.workspace.memory_profiler import MemoryProfiler
from src.infrastructure.engine.workspace.buffer_recycler import BufferRecycler

@pytest.fixture
def workspace_manager():
    mgr = WorkspaceManager(size_mb=128)
    yield mgr
    mgr.purge()

def test_workspace_allocation(workspace_manager):
    """Test DBO allocation in the workspace."""
    dbo = workspace_manager.allocate_dbo("test_dbo", 1024)
    assert dbo is not None
    assert len(dbo) == 1024
    assert workspace_manager.allocated == 1024
    assert workspace_manager.get_utilization() > 0

def test_dvd_channel_registration(workspace_manager):
    """Test 120fps DVD-channel registration."""
    success = workspace_manager.register_dvd_channel(1, buffer_size=4096)
    assert success is True
    assert 1 in workspace_manager._channels

    # Test sync beat
    workspace_manager.global_sync_beat()
    assert workspace_manager.last_sync_time > 0

def test_ubatching_slices():
    """Test micro-batch slicing logic."""
    batch = list(range(100))
    slices = UBatchingUtils.slice_batch(batch, min_slice=10)
    assert len(slices) == 10
    assert slices[0] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def test_memory_profiler():
    """Test real-time memory profiling."""
    profiler = MemoryProfiler()
    snapshot = profiler.take_snapshot("start")
    assert snapshot["usage_bytes"] >= 0

    profiler.take_snapshot("end")
    patterns = profiler.analyze_patterns()
    assert patterns["snapshot_count"] == 2

def test_buffer_recycler():
    """Test buffer reuse pools."""
    recycler = BufferRecycler()
    buf1 = recycler.acquire(1024) # Fits in 4KB class
    assert len(buf1) == 4096

    recycler.release(buf1)
    stats = recycler.get_stats()
    assert stats["4096"] == 1

    buf2 = recycler.acquire(1024)
    assert buf2 is buf1 # Should be recycled
