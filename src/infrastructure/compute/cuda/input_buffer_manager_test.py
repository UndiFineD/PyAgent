#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from infrastructure.compute.cuda.input_buffer_manager import BufferState, BufferSpec, BufferEntry, BufferPool, SimpleBufferPool, InputSlot, InputBufferManager, HierarchicalBufferPool, PredictiveBufferManager, create_input_buffer_manager


def test_bufferstate_basic():
    assert BufferState is not None


def test_bufferspec_basic():
    assert BufferSpec is not None


def test_bufferentry_basic():
    assert BufferEntry is not None


def test_bufferpool_basic():
    assert BufferPool is not None


def test_simplebufferpool_basic():
    assert SimpleBufferPool is not None


def test_inputslot_basic():
    assert InputSlot is not None


def test_inputbuffermanager_basic():
    assert InputBufferManager is not None


def test_hierarchicalbufferpool_basic():
    assert HierarchicalBufferPool is not None


def test_predictivebuffermanager_basic():
    assert PredictiveBufferManager is not None


def test_create_input_buffer_manager_basic():
    assert callable(create_input_buffer_manager)
