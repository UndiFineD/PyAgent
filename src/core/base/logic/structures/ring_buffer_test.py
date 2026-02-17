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

import pytest
from core.base.logic.structures.ring_buffer import RingBuffer, ThreadSafeRingBuffer, TimestampedValue, TimeSeriesBuffer, SlidingWindowAggregator


def test_ringbuffer_basic():
    assert RingBuffer is not None


def test_threadsaferingbuffer_basic():
    assert ThreadSafeRingBuffer is not None


def test_timestampedvalue_basic():
    assert TimestampedValue is not None


def test_timeseriesbuffer_basic():
    assert TimeSeriesBuffer is not None


def test_slidingwindowaggregator_basic():
    assert SlidingWindowAggregator is not None
