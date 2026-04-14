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
"""Tests for GET /api/metrics/system endpoint.

prj0000047 — conky-real-metrics.
TDD red phase: these tests are written BEFORE the endpoint exists and
must fail with HTTP 404 until @6code implements the endpoint.
"""

from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

import backend.app as _app_module
from backend.app import app

# ─── shared test client ──────────────────────────────────────────────────────

_CLIENT = TestClient(app)


# ─── psutil stub factories ───────────────────────────────────────────────────


def _vmem(
    total: int = 8 * 1024**3,
    used: int = 4 * 1024**3,
    percent: float = 50.0,
) -> MagicMock:
    m = MagicMock()
    m.total = total
    m.used = used
    m.percent = percent
    return m


def _net_counter(bytes_sent: int = 0, bytes_recv: int = 0) -> MagicMock:
    m = MagicMock()
    m.bytes_sent = bytes_sent
    m.bytes_recv = bytes_recv
    return m


def _disk_counter(read_bytes: int = 0, write_bytes: int = 0) -> MagicMock:
    m = MagicMock()
    m.read_bytes = read_bytes
    m.write_bytes = write_bytes
    return m


def _psutil_mock(
    cpu: float = 20.0,
    vmem: MagicMock | None = None,
    net: dict | None = None,
    disk: MagicMock | None = None,
) -> MagicMock:
    """Build a complete psutil module mock with sensible defaults."""
    mock = MagicMock()
    mock.cpu_percent.return_value = cpu
    mock.virtual_memory.return_value = vmem if vmem is not None else _vmem()
    mock.net_io_counters.return_value = net if net is not None else {}
    mock.disk_io_counters.return_value = disk if disk is not None else _disk_counter()
    return mock


# ─── tests ───────────────────────────────────────────────────────────────────


def test_endpoint_returns_200():
    """GET /api/metrics/system must return HTTP 200."""
    with patch("backend.app.psutil", create=True, new=_psutil_mock()):
        resp = _CLIENT.get("/api/metrics/system")

    assert resp.status_code == 200, f"Expected HTTP 200 but got {resp.status_code}. Endpoint not yet implemented (T3)."


def test_response_has_correct_shape():
    """Response JSON must include all five top-level contract keys."""
    with patch("backend.app.psutil", create=True, new=_psutil_mock()):
        resp = _CLIENT.get("/api/metrics/system")

    assert resp.status_code == 200
    body = resp.json()
    for key in ("cpu_percent", "memory", "network", "disk", "sampled_at"):
        assert key in body, f"Missing required key {key!r} in response: {body}"


def test_cpu_percent_is_in_valid_range():
    """`cpu_percent` must be a float in [0, 100]."""
    with patch("backend.app.psutil", create=True, new=_psutil_mock(cpu=73.2)):
        resp = _CLIENT.get("/api/metrics/system")

    assert resp.status_code == 200
    cpu = resp.json()["cpu_percent"]
    assert isinstance(cpu, (int, float)), f"cpu_percent is not numeric: {cpu!r}"
    assert 0 <= cpu <= 100, f"cpu_percent out of valid range: {cpu}"


def test_memory_fields_correct():
    """`memory` must contain `used_mb`, `total_mb`, `percent` with correct values."""
    total_bytes = 16 * 1024**3  # 16 GiB
    used_bytes = 6 * 1024**3  # 6 GiB

    mock = _psutil_mock(vmem=_vmem(total=total_bytes, used=used_bytes, percent=37.5))
    with patch("backend.app.psutil", create=True, new=mock):
        resp = _CLIENT.get("/api/metrics/system")

    assert resp.status_code == 200
    mem = resp.json()["memory"]

    assert "total_mb" in mem
    assert "used_mb" in mem
    assert "percent" in mem

    assert mem["total_mb"] == pytest.approx(16 * 1024, rel=0.01), (
        f"total_mb mismatch: expected ~{16 * 1024} MB, got {mem['total_mb']}"
    )
    assert mem["used_mb"] == pytest.approx(6 * 1024, rel=0.01), (
        f"used_mb mismatch: expected ~{6 * 1024} MB, got {mem['used_mb']}"
    )
    assert mem["total_mb"] > 0, "total_mb must be positive"
    assert 0 <= mem["percent"] <= 100, f"memory.percent out of range: {mem['percent']}"


def test_network_entries_have_required_fields():
    """`network` must be a list; each entry must have `interface`, `tx_kbps`, `rx_kbps`."""
    net = {"eth0": _net_counter(bytes_sent=1_048_576, bytes_recv=524_288)}
    mock = _psutil_mock(net=net)

    with patch("backend.app.psutil", create=True, new=mock):
        resp = _CLIENT.get("/api/metrics/system")

    assert resp.status_code == 200
    network = resp.json()["network"]
    assert isinstance(network, list), f"network must be a list, got {type(network)}"
    for entry in network:
        for field in ("interface", "tx_kbps", "rx_kbps"):
            assert field in entry, f"Missing field {field!r} in network entry: {entry}"
        assert isinstance(entry["tx_kbps"], (int, float)), "tx_kbps must be numeric"
        assert isinstance(entry["rx_kbps"], (int, float)), "rx_kbps must be numeric"


def test_loopback_and_virtual_interfaces_excluded():
    """Loopback and virtual interfaces must not appear in `network`."""
    net = {
        "lo": _net_counter(),  # Unix loopback
        "Loopback Pseudo-Interface 1": _net_counter(),  # Windows loopback
        "docker0": _net_counter(),  # docker bridge
        "veth4a2b": _net_counter(),  # veth pair
        "br-dead1234": _net_counter(),  # docker bridge br-*
        "eth0": _net_counter(),  # physical — should survive
    }
    mock = _psutil_mock(net=net)

    with patch("backend.app.psutil", create=True, new=mock):
        resp = _CLIENT.get("/api/metrics/system")

    assert resp.status_code == 200
    names = {entry["interface"] for entry in resp.json()["network"]}

    assert "lo" not in names, "'lo' must be filtered out"
    assert "docker0" not in names, "'docker0' must be filtered out"
    assert "veth4a2b" not in names, "'veth*' must be filtered out"
    assert "br-dead1234" not in names, "'br-*' must be filtered out"
    assert not any(n.lower().startswith("loopback") for n in names), "Loopback-named interfaces must be filtered out"


def test_disk_fields_are_non_negative_numbers():
    """`disk` must have `read_kbps` and `write_kbps` as non-negative floats."""
    mock = _psutil_mock(
        disk=_disk_counter(read_bytes=2_097_152, write_bytes=1_048_576),
    )

    with patch("backend.app.psutil", create=True, new=mock):
        resp = _CLIENT.get("/api/metrics/system")

    assert resp.status_code == 200
    disk = resp.json()["disk"]

    assert "read_kbps" in disk, "Missing 'read_kbps' in disk"
    assert "write_kbps" in disk, "Missing 'write_kbps' in disk"
    assert isinstance(disk["read_kbps"], (int, float)), "read_kbps must be numeric"
    assert isinstance(disk["write_kbps"], (int, float)), "write_kbps must be numeric"
    assert disk["read_kbps"] >= 0, f"read_kbps must be ≥ 0, got {disk['read_kbps']}"
    assert disk["write_kbps"] >= 0, f"write_kbps must be ≥ 0, got {disk['write_kbps']}"


def test_sampled_at_is_positive_and_recent():
    """`sampled_at` must be a positive float within 5 s of the request time."""
    mock = _psutil_mock()
    before = time.time()

    with patch("backend.app.psutil", create=True, new=mock):
        resp = _CLIENT.get("/api/metrics/system")

    after = time.time()
    assert resp.status_code == 200

    sampled_at = resp.json()["sampled_at"]
    assert isinstance(sampled_at, (int, float)), f"sampled_at must be numeric: {sampled_at!r}"
    assert sampled_at > 0, "sampled_at must be a positive epoch timestamp"
    assert before - 1 <= sampled_at <= after + 1, (
        f"sampled_at {sampled_at:.3f} not in expected window [{before:.3f}, {after:.3f}]"
    )


def test_first_call_returns_zero_rates():
    """On the first call (no prior sample), all KB/s fields must be 0.0."""
    # Reset differential state — setattr is safe even if attributes don't exist yet
    for attr, initial in [
        ("_prev_net", {}),
        ("_prev_net_ts", 0.0),
        ("_prev_disk", (0, 0)),
        ("_prev_disk_ts", 0.0),
    ]:
        setattr(_app_module, attr, initial)

    net = {"eth0": _net_counter(bytes_sent=5_000_000, bytes_recv=3_000_000)}
    mock = _psutil_mock(
        net=net,
        disk=_disk_counter(read_bytes=10_000_000, write_bytes=4_000_000),
    )

    with patch("backend.app.psutil", create=True, new=mock):
        resp = _CLIENT.get("/api/metrics/system")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code} — endpoint not yet implemented."
    body = resp.json()

    for entry in body["network"]:
        assert entry["tx_kbps"] == 0.0, f"First-call tx_kbps should be 0.0, got {entry['tx_kbps']}"
        assert entry["rx_kbps"] == 0.0, f"First-call rx_kbps should be 0.0, got {entry['rx_kbps']}"
    assert body["disk"]["read_kbps"] == 0.0, f"First-call disk read_kbps should be 0.0, got {body['disk']['read_kbps']}"
    assert body["disk"]["write_kbps"] == 0.0, (
        f"First-call disk write_kbps should be 0.0, got {body['disk']['write_kbps']}"
    )
