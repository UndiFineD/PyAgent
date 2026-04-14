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
"""Tests for the Rust async transport PyO3 bindings (prj0000056).

All tests skip gracefully when rust_core has not been compiled so the CI
suite never fails on environments that build Python-only.
"""

import struct

import pytest

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

pytestmark = pytest.mark.skipif(not HAS_RUST, reason="rust_core not compiled")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_transport(capacity: int = 64):
    """Instantiate a PyAsyncTransport with the given capacity."""
    return rust_core.PyAsyncTransport(capacity)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_module_importable():
    """rust_core module should be importable (guarded by pytestmark)."""
    assert rust_core is not None


def test_pyasynctransport_instantiation():
    """PyAsyncTransport(64) should construct without error."""
    t = _make_transport(64)
    assert t is not None


def test_get_capacity_small():
    """get_capacity() should return exactly the value passed at construction."""
    t = _make_transport(4)
    assert t.get_capacity() == 4


def test_get_capacity_large():
    """get_capacity() should handle large capacity values correctly."""
    t = _make_transport(1024)
    assert t.get_capacity() == 1024


def test_get_capacity_zero():
    """get_capacity() should return 0 when capacity=0 is requested."""
    t = _make_transport(0)
    assert t.get_capacity() == 0


def test_create_channel_returns_two_elements():
    """create_channel() must return a 2-element tuple."""
    t = _make_transport(64)
    result = t.create_channel()
    assert len(result) == 2


def test_create_channel_send_handle_encodes_capacity():
    """First element of create_channel() encodes the capacity as LE u64."""
    capacity = 32
    t = _make_transport(capacity)
    send_handle, _ = t.create_channel()
    decoded = struct.unpack_from("<Q", bytes(send_handle))[0]
    assert decoded == capacity


def test_create_channel_recv_handle_encodes_capacity():
    """Second element of create_channel() encodes the capacity as LE u64."""
    capacity = 128
    t = _make_transport(capacity)
    _, recv_handle = t.create_channel()
    decoded = struct.unpack_from("<Q", bytes(recv_handle))[0]
    assert decoded == capacity


def test_multiple_instances_independent():
    """Multiple PyAsyncTransport instances should not share state."""
    t1 = _make_transport(8)
    t2 = _make_transport(256)
    assert t1.get_capacity() == 8
    assert t2.get_capacity() == 256
