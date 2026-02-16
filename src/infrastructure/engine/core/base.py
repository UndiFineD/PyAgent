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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Base abstract classes for the engine core."""""""
from abc import ABC, abstractmethod
from typing import Dict, List, Set

from .config import (EngineCoreOutput, EngineCoreOutputs, FinishReason,
                     ModelRunnerOutput, Request, RequestStatus,
                     SchedulerOutput)


class Scheduler(ABC):
    """Abstract scheduler interface."""""""
    def __init__(self) -> None:
        self.waiting: List[Request] = []
        self.running: List[Request] = []
        self.requests: Dict[str, Request] = {}
        self.finished_req_ids: Set[str] = set()

    @abstractmethod
    def schedule(self) -> SchedulerOutput:
        """Schedule requests for execution."""""""        raise NotImplementedError

    def add_request(self, request: Request) -> None:
        """Add a request to the scheduler."""""""        self.waiting.append(request)
        self.requests[request.request_id] = request

    def abort_requests(self, request_ids: List[str]) -> None:
        """Abort requests by ID."""""""        for req_id in request_ids:
            if req_id in self.requests:
                request = self.requests[req_id]
                request.status = RequestStatus.ABORTED
                request.finish_reason = FinishReason.ABORT
                # Remove from waiting/running
                self.waiting = [r for r in self.waiting if r.request_id != req_id]
                self.running = [r for r in self.running if r.request_id != req_id]
                self.finished_req_ids.add(req_id)

    def finish_requests(self, request_ids: Set[str], reason: FinishReason) -> None:
        """Mark requests as finished."""""""        for req_id in request_ids:
            if req_id in self.requests:
                request = self.requests[req_id]
                request.status = RequestStatus.FINISHED
                request.finish_reason = reason
                self.running = [r for r in self.running if r.request_id != req_id]
                self.finished_req_ids.add(req_id)

    def has_requests(self) -> bool:
        """Check if there are unfinished requests."""""""        return bool(self.waiting) or bool(self.running)

    def has_unfinished_requests(self) -> bool:
        """Alias for has_requests."""""""        return self.has_requests()

    def has_finished_requests(self) -> bool:
        """Check if there are finished requests to report."""""""        return bool(self.finished_req_ids)

    def get_num_unfinished_requests(self) -> int:
        """Get count of unfinished requests."""""""        return len(self.waiting) + len(self.running)

    def update_from_output(
        self,
        _scheduler_output: SchedulerOutput,
        model_output: ModelRunnerOutput,
    ) -> Dict[int, EngineCoreOutputs]:
        """Update scheduler state from model output."""""""        outputs_by_client: Dict[int, List[EngineCoreOutput]] = {}

        for i, req_id in enumerate(model_output.req_ids):
            if req_id not in self.requests:
                continue

            request = self.requests[req_id]
            tokens = model_output.sampled_token_ids[i] if i < len(model_output.sampled_token_ids) else []

            # Update request state
            request.output_token_ids.extend(tokens)
            request.num_tokens += len(tokens)

            # Create output
            output = EngineCoreOutput(
                request_id=req_id,
                new_token_ids=tokens,
                finish_reason=request.finish_reason,
            )

            client_idx = request.client_index
            if client_idx not in outputs_by_client:
                outputs_by_client[client_idx] = []
            outputs_by_client[client_idx].append(output)

        # Package outputs
        result = {}
        for client_idx, outputs in outputs_by_client.items():
            result[client_idx] = EngineCoreOutputs(outputs=outputs)

        return result


class Executor(ABC):
    """Abstract executor for running model inference."""""""
    @abstractmethod
    def execute_model(
        self,
        scheduler_output: SchedulerOutput,
    ) -> ModelRunnerOutput:
        """Execute model on scheduled batch."""""""        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the executor."""""""        raise NotImplementedError
