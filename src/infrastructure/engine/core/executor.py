# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Standard executor implementations."""

from .config import SchedulerOutput, ModelRunnerOutput
from .base import Executor


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
        pass
