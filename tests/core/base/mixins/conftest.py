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

"""Shared pytest fixtures for mixin parity and failure-path checks."""

from __future__ import annotations

import pytest

from tests.core.base.mixins.parity_cases import (
    AuditParityHosts,
    ReplayParityHosts,
    SandboxParityHosts,
    make_audit_parity_hosts,
    make_replay_parity_hosts,
    make_sandbox_parity_hosts,
)


@pytest.fixture
def audit_parity_hosts() -> AuditParityHosts:
    """Provide legacy and canonical audit hosts for parity assertions.

    Returns:
        Legacy and canonical audit host pair.

    """
    return make_audit_parity_hosts()


@pytest.fixture
def sandbox_parity_hosts() -> SandboxParityHosts:
    """Provide legacy and canonical sandbox hosts for parity assertions.

    Returns:
        Legacy and canonical sandbox host pair.

    """
    return make_sandbox_parity_hosts()


@pytest.fixture
def replay_parity_hosts() -> ReplayParityHosts:
    """Provide legacy and canonical replay hosts for parity assertions.

    Returns:
        Legacy and canonical replay host pair.

    """
    return make_replay_parity_hosts()
