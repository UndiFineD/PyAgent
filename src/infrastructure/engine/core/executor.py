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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Standard executor implementations."""

from .base import Executor
from .config import ModelRunnerOutput, SchedulerOutput


class MockExecutor(Executor):
    """Mock executor for testing."""

    def __init__(self, tokens_per_step: int = 1):
        self.tokens_per_step = tokens_per_step

    def execute_model(
        self,
        scheduler_output: SchedulerOutput,
    ) -> ModelRunnerOutput:
        """Generate mock tokens."""
        output = ModelRunnerOutput()

        for request in scheduler_output.scheduled_requests:
            output.req_ids.append(request.request_id)
            output.req_id_to_index[request.request_id] = len(output.req_ids) - 1
            # Generate mock tokens
            output.sampled_token_ids.append([1000] * self.tokens_per_step)

        return output

    def shutdown(self) -> None:
        """No-op shutdown."""
