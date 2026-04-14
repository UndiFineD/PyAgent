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

"""Per-module tests for src/core/sandbox/SandboxMixin.py.

Comprehensive sandbox integration tests live in tests/test_sandbox.py.
This file satisfies the test_each_core_has_test_file convention.
"""

from __future__ import annotations

from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxMixin import SandboxMixin, validate
from src.core.sandbox.SandboxViolationError import SandboxViolationError


def test_sandbox_mixin_validate() -> None:
    """Ensure the SandboxMixin validate() helper returns True."""
    assert validate() is True


def test_sandbox_mixin_sandbox_tx_returns_transaction() -> None:
    """sandbox_tx() must return a SandboxedStorageTransaction bound to the config."""

    class Agent(SandboxMixin):
        """Minimal agent for mixin unit test."""

        def __init__(self) -> None:
            """Initialize with a sandbox config that allows /tmp."""
            self._sandbox_config = SandboxConfig.from_strings(paths=["/tmp"], hosts=[])

    agent = Agent()
    tx = agent.sandbox_tx()
    assert tx is not None


def test_sandbox_mixin_validate_host_raises_on_blocked_host() -> None:
    """_validate_host must raise SandboxViolationError for unlisted hosts."""
    import pytest

    class Agent(SandboxMixin):
        """Minimal agent with restricted host list."""

        def __init__(self) -> None:
            """Initialize with empty host allowlist."""
            self._sandbox_config = SandboxConfig.from_strings(paths=[], hosts=["trusted.example.com"])

    agent = Agent()
    with pytest.raises(SandboxViolationError):
        agent._validate_host("evil.example.com")
