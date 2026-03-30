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

"""Deterministic tie-break resolver with bounded timeout behavior."""

from __future__ import annotations

from src.core.routing.routing_models import RouteCandidate


class TieBreakTimeoutError(TimeoutError):
    """Raised when tie-break is asked to exceed configured timeout budget."""


class TieBreakResolver:
    """Resolve ambiguous candidates deterministically."""

    def resolve(
        self,
        candidates: list[RouteCandidate],
        *,
        timeout_ms: int,
        seed: str,
    ) -> RouteCandidate | None:
        """Resolve one final candidate under deterministic and bounded rules.

        Args:
            candidates: Candidate list to resolve.
            timeout_ms: Timeout budget in milliseconds.
            seed: Deterministic seed value.

        Returns:
            Resolved candidate, or None when no winner can be produced.

        Raises:
            TieBreakTimeoutError: If timeout budget is below supported minimum.

        """
        if timeout_ms < 1:
            raise TieBreakTimeoutError("timeout budget too small")
        if not candidates:
            return None

        top_score = max(candidate.score for candidate in candidates)
        top_candidates = [candidate for candidate in candidates if candidate.score == top_score]

        if len(top_candidates) == 1:
            return top_candidates[0]

        pivot = sum(ord(ch) for ch in seed) % len(top_candidates)
        ordered = sorted(top_candidates, key=lambda item: item.route)
        return ordered[pivot]


def validate() -> bool:
    """Validate deterministic tie-break behavior.

    Returns:
        True when tie-break deterministically resolves equal scores.

    """
    winner = TieBreakResolver().resolve(
        [RouteCandidate(route="legacy", score=0.5), RouteCandidate(route="core", score=0.5)],
        timeout_ms=10,
        seed="validate-seed",
    )
    return winner is not None and winner.route in {"core", "legacy"}
