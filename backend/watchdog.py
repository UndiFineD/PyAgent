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

"""AgentWatchdog — per-agent execution timeout with retry budget and dead-letter queue."""
from __future__ import annotations

import asyncio
import time
from collections import defaultdict
from typing import Any


class AgentWatchdog:
    """Runs async agent tasks with a configurable timeout and retry budget.

    On timeout the task is retried up to *max_retries* times; if the budget is
    exhausted the task entry is appended to the dead-letter queue (DLQ).
    """

    def __init__(self, timeout_s: float = 30.0, max_retries: int = 3) -> None:
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self._retry_counts: dict[str, int] = defaultdict(int)
        self._dlq: list[dict] = []

    async def run(self, agent_id: str, coro: Any) -> dict:
        """Execute *coro* for *agent_id* with timeout and retry logic.

        Returns::
            {"status": "ok", "agent_id": agent_id, "result": <coro_result>}
            {"status": "dead_letter", "agent_id": agent_id, "retries": n}
        """
        try:
            result = await asyncio.wait_for(coro, timeout=self.timeout_s)
            return {"status": "ok", "agent_id": agent_id, "result": result}
        except asyncio.TimeoutError:
            self._retry_counts[agent_id] += 1
            if self._retry_counts[agent_id] < self.max_retries:
                # Caller can retry; we surface the information via the return value
                # rather than raising so the caller decides the retry strategy.
                return {
                    "status": "timeout",
                    "agent_id": agent_id,
                    "retries": self._retry_counts[agent_id],
                }
            entry = {
                "agent_id": agent_id,
                "retries": self._retry_counts[agent_id],
                "timestamp": time.time(),
            }
            self._dlq.append(entry)
            return {"status": "dead_letter", "agent_id": agent_id, "retries": self._retry_counts[agent_id]}

    def status(self) -> dict:
        """Return a summary of watchdog state."""
        return {
            "timeout_s": self.timeout_s,
            "max_retries": self.max_retries,
            "dlq_size": len(self._dlq),
            "retry_counts": dict(self._retry_counts),
        }

    @property
    def dead_letter_queue(self) -> list[dict]:
        """Read-only view of the DLQ entries."""
        return list(self._dlq)


# Module-level singleton used by the FastAPI app.
watchdog = AgentWatchdog()
