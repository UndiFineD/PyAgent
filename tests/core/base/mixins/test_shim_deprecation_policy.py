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

"""Red tests for shim deprecation policy contract (AC-MX-003, T006)."""

from __future__ import annotations

from importlib import import_module


def test_legacy_audit_shim_declares_removal_wave_metadata() -> None:
    """Require audit shim to declare deterministic removal wave metadata."""
    module = import_module("src.core.audit.AuditTrailMixin")
    expected_wave = "W4"
    actual_wave = getattr(module, "__shim_removal_wave__", None)
    assert actual_wave == expected_wave, f"Expected __shim_removal_wave__={expected_wave}, got {actual_wave!r}"


def test_legacy_sandbox_shim_declares_removal_wave_metadata() -> None:
    """Require sandbox shim to declare deterministic removal wave metadata."""
    module = import_module("src.core.sandbox.SandboxMixin")
    expected_wave = "W4"
    actual_wave = getattr(module, "__shim_removal_wave__", None)
    assert actual_wave == expected_wave, f"Expected __shim_removal_wave__={expected_wave}, got {actual_wave!r}"


def test_legacy_replay_shim_declares_removal_wave_metadata() -> None:
    """Require replay shim to declare deterministic removal wave metadata."""
    module = import_module("src.core.replay.ReplayMixin")
    expected_wave = "W4"
    actual_wave = getattr(module, "__shim_removal_wave__", None)
    assert actual_wave == expected_wave, f"Expected __shim_removal_wave__={expected_wave}, got {actual_wave!r}"
