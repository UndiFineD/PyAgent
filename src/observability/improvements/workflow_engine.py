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
from src.core.base.version import VERSION
from .improvement import Improvement
from .transition_result import TransitionResult

__version__ = VERSION


class WorkflowEngine:
    """Manages improvement workflow transitions."""

    def __init__(self) -> None:
        self.states: list[str] = [
            "pending",
            "in_progress",
            "completed",
            "blocked",
        ]
        self._transitions: dict[str, list[str]] = {
            "pending": ["in_progress", "blocked"],
            "in_progress": ["completed", "blocked"],
            "blocked": ["in_progress"],
            "completed": [],
        }

    def transition(
        self, improvement: Improvement, from_status: str, to_status: str
    ) -> TransitionResult:
        allowed = self._transitions.get(from_status, [])
        if to_status not in allowed:
            return TransitionResult(success=False, message="Invalid transition")

        # Tests expect string status updates.
        setattr(improvement, "status", to_status)
        return TransitionResult(success=True)
