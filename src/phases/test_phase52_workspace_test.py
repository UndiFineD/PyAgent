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
from .test_phase52_workspace import workspace_manager, test_workspace_allocation, test_dvd_channel_registration, test_ubatching_slices, test_memory_profiler, test_buffer_recycler


def test_workspace_manager_basic():
    assert callable(workspace_manager)


def test_test_workspace_allocation_basic():
    assert callable(test_workspace_allocation)


def test_test_dvd_channel_registration_basic():
    assert callable(test_dvd_channel_registration)


def test_test_ubatching_slices_basic():
    assert callable(test_ubatching_slices)


def test_test_memory_profiler_basic():
    assert callable(test_memory_profiler)


def test_test_buffer_recycler_basic():
    assert callable(test_buffer_recycler)
