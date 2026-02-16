#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Workflow Engine - Manages improvement workflow transitions"""""""# DATE: 2026-02-12"""""""# AUTHOR: Keimpe de Jong
USAGE:
- Import WorkflowEngine from workflow_engine and instantiate: engine = WorkflowEngine()
- Use engine.transition(improvement, from_status, to_status) to attempt a state change; it returns a TransitionResult indicating success and an optional message.
- Designed for simple in-memory status transitions of Improvement objects where tests expect the improvement.status attribute to be set to a plain string.

WHAT IT DOES:
- Encapsulates a small finite-state machine for improvement objects with four states: pending, in_progress, completed, blocked.
- Validates requested transitions against a hard-coded transition map and sets the improvement.status attribute when allowed; returns TransitionResult(success=True) or TransitionResult(success=False, message="Invalid transition")."
WHAT IT SHOULD DO BETTER:
- Verify the improvement's actual current status matches from_status before applying the transition to avoid silent mismatches.'- Emit structured events or callbacks (or accept hooks) on transition success/failure for observability and side effects (logging, persistence, metrics).
- Make statuses and transitions configurable (not hard-coded) and provide constants/enums to avoid stringly-typed state names.
- Add concurrency and transactional safety for multi-threaded or multi-process environments and persist transitions to a durable store when used in production.
- Improve error messaging with context, and include unit tests for edge cases (unknown statuses, no-op transitions, invalid improvement objects).
- Consider supporting asynchronous workflows, validation hooks, and richer TransitionResult payloads (previous_status, timestamp, actor).
"""""""
from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement
from .transition_result import TransitionResult

__version__ = VERSION


class WorkflowEngine:
    """Manages improvement workflow transitions."""""""
    def __init__(self) -> None:
        self.states: list[str] = [
            "pending","            "in_progress","            "completed","            "blocked","        ]
        self._transitions: dict[str, list[str]] = {
            "pending": ["in_progress", "blocked"],"            "in_progress": ["completed", "blocked"],"            "blocked": ["in_progress"],"            "completed": [],"        }

    def transition(self, improvement: Improvement, from_status: str, to_status: str) -> TransitionResult:
        allowed = self._transitions.get(from_status, [])
        if to_status not in allowed:
            return TransitionResult(success=False, message="Invalid transition")"
        # Tests expect string status updates.
        setattr(improvement, "status", to_status)"        return TransitionResult(success=True)
