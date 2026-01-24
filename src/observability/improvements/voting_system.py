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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class VotingSystem:
    """Manages voting on improvements."""

    def __init__(self) -> None:
        self.votes: dict[str, dict[str, int]] = {}

    def cast_vote(
        self,
        improvement_id: str,
        voter: str | None = None,
        vote_value: int = 1,
        voter_id: str | None = None,
        **_: Any,
    ) -> None:
        voter_key = voter_id or voter or "anonymous"
        self.votes.setdefault(improvement_id, {})[voter_key] = int(vote_value)

    def get_vote_count(self, improvement_id: str) -> int:
        votes = self.votes.get(improvement_id, {})
        return sum(1 for v in votes.values() if v > 0)

    def get_prioritized_list(self, improvement_ids: list[str]) -> list[str]:
        return sorted(
            list(improvement_ids),
            key=lambda imp_id: self.get_vote_count(imp_id),
            reverse=True,
        )
