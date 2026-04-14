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

"""Tie-break deterministic and timeout behavior tests."""

from __future__ import annotations

import pytest

from src.core.routing.routing_models import RouteCandidate
from src.core.routing.tie_break_resolver import TieBreakResolver, TieBreakTimeoutError


def test_tie_break_is_deterministic_for_same_seed() -> None:
    """Tie-break output should remain stable for repeated runs with same seed."""
    resolver = TieBreakResolver()
    candidates = [RouteCandidate(route="legacy", score=0.5), RouteCandidate(route="core", score=0.5)]

    first = resolver.resolve(candidates, timeout_ms=20, seed="req-deterministic")
    second = resolver.resolve(candidates, timeout_ms=20, seed="req-deterministic")

    assert first is not None
    assert second is not None
    assert first.route == second.route


def test_tie_break_timeout_raises_typed_error() -> None:
    """Tiny timeout budgets should raise deterministic timeout error."""
    resolver = TieBreakResolver()
    candidates = [RouteCandidate(route="legacy", score=0.5), RouteCandidate(route="core", score=0.5)]

    with pytest.raises(TieBreakTimeoutError):
        resolver.resolve(candidates, timeout_ms=0, seed="req-timeout")
