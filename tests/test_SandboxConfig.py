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

"""Per-module tests for src/core/sandbox/SandboxConfig.py.

Comprehensive sandbox integration tests live in tests/test_sandbox.py.
This file satisfies the test_each_core_has_test_file convention.
"""

from __future__ import annotations

from src.core.sandbox.SandboxConfig import SandboxConfig, validate


def test_sandbox_config_validate() -> None:
    """Ensure the SandboxConfig validate() helper returns True."""
    assert validate() is True


def test_sandbox_config_from_strings_round_trips() -> None:
    """SandboxConfig.from_strings must produce matching allowed_paths and allowed_hosts."""
    cfg = SandboxConfig.from_strings(paths=["/tmp/safe"], hosts=["localhost"])
    assert len(cfg.allowed_paths) == 1
    assert len(cfg.allowed_hosts) == 1
    assert cfg.allowed_hosts[0] == "localhost"


def test_sandbox_config_agent_id_auto_generated() -> None:
    """agent_id must be a non-empty UUID string when not supplied."""
    cfg = SandboxConfig.from_strings(paths=[], hosts=[])
    assert isinstance(cfg.agent_id, str)
    assert len(cfg.agent_id) == 36  # UUID4 string length
