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

"""Per-module red tests for ShadowExecutionCore contract module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from tests.test_shadow_replay import _build_envelope, _require_symbol


@dataclass
class _Tx:
    """Track commit and rollback operations in shadow-core smoke tests."""

    committed: bool = False
    rolled_back: bool = False

    async def commit(self) -> None:
        """Record commit call."""
        self.committed = True

    async def rollback(self) -> None:
        """Record rollback call."""
        self.rolled_back = True


def _make_shadow_core() -> Any:
    """Build ShadowExecutionCore with transaction factories.

    Yields:
        A configured shadow-core instance.

    """
    shadow_execution_core_cls = _require_symbol("ShadowExecutionCore", "ShadowExecutionCore")

    def _factory() -> _Tx:
        """Create trackable transaction recorders."""
        return _Tx()

    return shadow_execution_core_cls(
        memory_tx_factory=_factory,
        storage_tx_factory=_factory,
        process_tx_factory=_factory,
        context_tx_factory=_factory,
    )


@pytest.mark.asyncio
async def test_shadow_execution_core_execute_envelope_returns_structured_result() -> None:
    """Verify execute_envelope returns a structured success/failure object."""
    shadow_core = _make_shadow_core()
    result = await shadow_core.execute_envelope(_build_envelope(sequence_no=1, session_id="s-module-shadow"))
    assert hasattr(result, "success")
