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

"""
Test Phase58 Predictive module.
"""
# Tests for Phase 58: Predictive Workspace & Pre-allocation

import pytest
from src.infrastructure.engine.workspace.workspace_manager import WorkspaceManager
from src.infrastructure.engine.workspace.predictive_workspace import PredictiveWorkspace


def test_predictive_pattern_analysis():
    # Initialize workspace
    wm = WorkspaceManager(size_mb=100)
    pw = PredictiveWorkspace(wm)

    # Record some allocations
    sizes = [1024, 1024, 2048, 1024, 4096]
    for s in sizes:
        pw.record_allocation(s)

    next_req = pw.predict_next_batch_requirement()
    # Expectation: between the mean and max
    assert next_req > 1000

    patterns = pw.analyze_patterns()
    # Top pattern should be 1024 (frequency 3)
    assert patterns["top_patterns"][0][0] == 1024


@pytest.mark.asyncio
async def test_pre_warm_and_reuse():
    # Reset Singleton (for testing purposes, we usually avoid this but here we need fresh state)
    WorkspaceManager._instance = None
    wm = WorkspaceManager(size_mb=100)

    # Pre-warm a buffer
    size = 5000
    await wm.predictive.pre_warm_buffers([size])

    assert len(wm.predictive.pre_allocated_buffers[size]) == 1

    # Request an allocation of the same size
    # This should trigger a "cache hit" in the predictive workspace
    buf = wm.allocate_dbo("test_dbo", size)

    assert buf is not None
    assert wm.predictive.cache_hits == 1
    assert len(wm.predictive.pre_allocated_buffers[size]) == 0


@pytest.mark.asyncio
async def test_moving_average_prediction():
    wm = WorkspaceManager(size_mb=50)
    pw = PredictiveWorkspace(wm, window_size=10)

    # Upward trend
    for i in range(1, 6):
        pw.record_allocation(i * 1000)

    prediction = pw.predict_next_batch_requirement()
    # Average of [1k, 2k, 3k, 4k, 5k] is 3k. With 1.2 margin = 3.6k.
    # Weighted average will be higher than 3k.
    assert prediction > 3500
