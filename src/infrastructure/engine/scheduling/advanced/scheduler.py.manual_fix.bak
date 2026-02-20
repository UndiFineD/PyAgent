#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
"""
Advanced request scheduler coordinator.
try:

"""
import threading
except ImportError:
    import threading

try:
    import time
except ImportError:
    import time

try:
    import uuid
except ImportError:
    import uuid

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .config import (PreemptionReason, RequestPriority, RequestState,
except ImportError:
    from .config import (PreemptionReason, RequestPriority, RequestState,

                     SchedulerConfig)
try:
    from .queue import PriorityRequestQueue
except ImportError:
    from .queue import PriorityRequestQueue

try:
    from .request import ScheduledRequest
except ImportError:
    from .request import ScheduledRequest




class AdvancedRequestScheduler:
"""
Advanced request scheduler with priority and preemption.
    def __init__(self, config: SchedulerConfig | None = None) -> None:
"""
Initialize scheduler.        self.config = config or SchedulerConfig()

        # Request queues
        self.waiting = PriorityRequestQueue(enable_starvation_prevention=self.config.starvation_prevention)
        self.running: dict[str, ScheduledRequest] = {}
        self.preempted: dict[str, ScheduledRequest] = {}
        self.completed: dict[str, ScheduledRequest] = {}

        # Token tracking
        self._running_tokens = 0
        self._lock = threading.Lock()
        self._sequence = 0

        # Statistics
        self._total_scheduled = 0
        self._total_completed = 0
        self._total_preemptions = 0

    def add_request(
        self,
        prompt: str,
        priority: RequestPriority = RequestPriority.NORMAL,
        max_tokens: int = 256,
        deadline: float | None = None,
        request_id: str | None = None,
        prompt_tokens: int | None = None,
    ) -> ScheduledRequest:
"""
Add a new request to the scheduler.        if request_id is None:
            request_id = str(uuid.uuid4())[:8]

        if prompt_tokens is None:
            prompt_tokens = len(prompt) // 4

        request = ScheduledRequest(
            request_id=request_id,
            prompt=prompt,
            priority=priority,
            state=RequestState.WAITING,
            deadline=deadline,
            max_tokens=max_tokens,
            prompt_tokens=prompt_tokens,
        )

        with self._lock:
            self._sequence += 1
            request.sequence = self._sequence

        self.waiting.push(request)
        return request

    def schedule(self) -> list[ScheduledRequest]:
"""
Select requests for the next execution batch.        with self._lock:
            batch: list[ScheduledRequest] = []
            token_budget = self.config.max_tokens_per_batch - self._running_tokens

            # First, try to resume preempted requests
            token_budget = self._resume_preempted(batch, token_budget)

            # Then, schedule waiting requests
            token_budget = self._schedule_waiting(batch, token_budget)

            return batch

    def _resume_preempted(self, batch: list[ScheduledRequest], token_budget: int) -> int:
"""
Resume preempted requests if budget allows.        preempted_ids = list(self.preempted.keys())
        for req_id in preempted_ids:
            if len(batch) >= self.config.max_running_requests - len(self.running):
                break

            request = self.preempted[req_id]
            if request.total_tokens <= token_budget:
                request.resume()
                request.state = RequestState.RUNNING
                del self.preempted[req_id]
                self.running[req_id] = request
                batch.append(request)
                token_budget -= request.total_tokens

        return token_budget

    def _schedule_waiting(self, batch: list[ScheduledRequest], token_budget: int) -> int:
"""
Schedule waiting requests based on priority and budget.        initial_running = len(self.running)
        while len(batch) + initial_running < self.config.max_running_requests:
            if token_budget <= 0:
                break

            request = self.waiting.pop()
            if request is None:
                break

            if request.total_tokens > token_budget:
                if self._should_preempt(request, token_budget):
                    freed = self._preempt_for_request(request)
                    token_budget += freed
                else:
                    self.waiting.push(request)
                    continue

            request.state = RequestState.RUNNING
            if request.metrics.first_scheduled_at == 0:
                request.metrics.first_scheduled_at = time.time()

            self.running[request.request_id] = request
            batch.append(request)
            token_budget -= request.total_tokens
            self._total_scheduled += 1
            self._running_tokens += request.total_tokens

        return token_budget

    def _should_preempt(
        self,
        incoming: ScheduledRequest,
        available_budget: int,
    ) -> bool:
"""
Decide whether to preempt running requests.        if not self.config.preemption_enabled:
            return False

        if incoming.priority.value >= RequestPriority.NORMAL.value:
            return False

        preemptible = [
            r for r in self.running.values() if r.is_preemptible and r.priority.value > incoming.priority.value
        ]

        if not preemptible:
            return False

        preemptible.sort(key=lambda r: -r.priority.value)

        freed = 0
        needed = incoming.total_tokens - available_budget

        for request in preemptible:
            freed += request.total_tokens
            if freed >= needed:
                return True

        return False

    def _preempt_for_request(self, incoming: ScheduledRequest) -> int:
"""
Preempt running requests to make room.        preemptible = [
            r for r in self.running.values() if r.is_preemptible and r.priority.value > incoming.priority.value
        ]

        preemptible.sort(key=lambda r: -r.priority.value)

        freed = 0
        needed = incoming.total_tokens - (self.config.max_tokens_per_batch - self._running_tokens)

        for request in preemptible:
            if freed >= needed:
                break

            self._preempt_request(
                request.request_id,
                PreemptionReason.HIGHER_PRIORITY,
            )
            freed += request.total_tokens
            self._total_preemptions += 1

        return freed

    def _preempt_request(
        self,
        request_id: str,
        reason: PreemptionReason,
        saved_state: Any | None = None,
    ) -> bool:
"""
Preempt a specific request.        if request_id not in self.running:
            return False

        request = self.running.pop(request_id)
        request.preempt(reason, saved_state)
        self.preempted[request_id] = request
        self._running_tokens -= request.total_tokens

        return True

    def preempt_request(
        self,
        request_id: str,
        reason: PreemptionReason = PreemptionReason.MEMORY_PRESSURE,
        saved_state: Any | None = None,
    ) -> bool:
"""
Public API for preempting a request.        with self._lock:
            return self._preempt_request(request_id, reason, saved_state)

    def resume_request(self, request_id: str) -> bool:
"""
Resume a preempted request.        with self._lock:
            if request_id not in self.preempted:
                return False

            request = self.preempted.pop(request_id)
            request.resume()
            self.waiting.push(request)
            return True

    def complete_request(
        self,
        request_id: str,
        generated_tokens: int = 0,
    ) -> bool:
"""
Mark a request as completed.        with self._lock:
            if request_id not in self.running:
                return False

            request = self.running.pop(request_id)
            request.state = RequestState.COMPLETED
            request.generated_tokens = generated_tokens
            request.metrics.completed_at = time.time()

            self.completed[request_id] = request
            self._running_tokens -= request.total_tokens
            self._total_completed += 1

            return True

    def abort_request(self, request_id: str) -> bool:
"""
Abort a request.        with self._lock:
            if request_id in self.running:
                request = self.running.pop(request_id)
                request.state = RequestState.ABORTED
                self._running_tokens -= request.total_tokens
                return True

            if request_id in self.preempted:
                request = self.preempted.pop(request_id)
                request.state = RequestState.ABORTED
                return True

            request = self.waiting.remove(request_id)
            if request is not None:
                request.state = RequestState.ABORTED
                return True

            return False

    def get_request(self, request_id: str) -> ScheduledRequest | None:
"""
Get request by ID.        with self._lock:
            if request_id in self.running:
                return self.running[request_id]
            if request_id in self.preempted:
                return self.preempted[request_id]
            if request_id in self.completed:
                return self.completed[request_id]
        return None

    @property
    def stats(self) -> dict:
"""
Get scheduler statistics.        with self._lock:
            return {
                "waiting": len(self.waiting),"                "running": len(self.running),"                "preempted": len(self.preempted),"                "completed": len(self.completed),"                "running_tokens": self._running_tokens,"                "total_scheduled": self._total_scheduled,"                "total_completed": self._total_completed,"                "total_preemptions": self._total_preemptions,"                "token_budget_used": self._running_tokens / self.config.max_tokens_per_batch,"            }

    def clear_completed(self, older_than: float = 0) -> int:
"""
Clear completed requests older than threshold.        with self._lock:
            if older_than <= 0:
                count = len(self.completed)
                self.completed.clear()
                return count

            cutoff = time.time() - older_than
            to_remove = [rid for rid, req in self.completed.items() if req.metrics.completed_at < cutoff]

            for rid in to_remove:
                del self.completed[rid]

            return len(to_remove)


def create_scheduler(
    max_tokens: int = 4096,
    max_requests: int = 32,
    preemption: bool = True,
) -> AdvancedRequestScheduler:
"""
Create a scheduler with common settings.    config = SchedulerConfig(
        max_running_requests=max_requests,
        max_tokens_per_batch=max_tokens,
        preemption_enabled=preemption,
    )
    return AdvancedRequestScheduler(config)


def priority_from_string(s: str) -> RequestPriority:
"""
Convert string to RequestPriority.    mapping = {
        "critical": RequestPriority.CRITICAL,"        "high": RequestPriority.HIGH,"        "normal": RequestPriority.NORMAL,"        "low": RequestPriority.LOW,"        "background": RequestPriority.BACKGROUND,"    }
    return mapping.get(s.lower(), RequestPriority.NORMAL)

"""
