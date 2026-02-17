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
"""Standard scheduler implementations.
from .base import Scheduler
from .config import RequestStatus, SchedulerOutput




class SimpleScheduler(Scheduler):
    """Simple FCFS scheduler implementation.
    def __init__(self, max_batch_size: int = 32, max_tokens: int = 4096) -> None:
        super().__init__()
        self.max_batch_size = max_batch_size
        self.max_tokens = max_tokens

    def schedule(self) -> SchedulerOutput:
        """Schedule waiting requests for execution.        output = SchedulerOutput()

        # Move waiting to running up to batch size
        total_tokens = sum(r.num_tokens - r.num_computed_tokens for r in self.running)

        while self.waiting and len(self.running) < self.max_batch_size:
            request = self.waiting[0]
            tokens_needed = request.num_tokens - request.num_computed_tokens

            if total_tokens + tokens_needed > self.max_tokens:
                break

            self.waiting.pop(0)
            request.status = RequestStatus.RUNNING
            self.running.append(request)
            total_tokens += tokens_needed

        # Build output
        for request in self.running:
            output.scheduled_requests.append(request)
            tokens = request.num_tokens - request.num_computed_tokens
            output.num_scheduled_tokens[request.request_id] = tokens
            output.total_num_scheduled_tokens += tokens

            if request.num_computed_tokens == 0:
                output.num_prefill_tokens += tokens
            else:
                output.num_decode_tokens += tokens

        return output
