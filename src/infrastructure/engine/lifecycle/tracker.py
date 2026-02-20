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


try:
    from dataclasses import dataclass, field
"""
except ImportError:

"""
from dataclasses import dataclass, field

try:
    from typing import Any, Dict, List, Optional
except ImportError:
    from typing import Any, Dict, List, Optional


try:
    from .enums import FinishReason
except ImportError:
    from .enums import FinishReason

try:
    from .request import Request
except ImportError:
    from .request import Request



@dataclass
class RequestTracker:
"""
Comprehensive tracking for request lifecycle metrics.

    This class aggregates statistics across all requests for
    monitoring and optimization.
"""

    # Counters
    total_requests: int = 0
    completed_requests: int = 0
    aborted_requests: int = 0
    error_requests: int = 0

    # Timing aggregates (in seconds)
    total_queue_time: float = 0.0
    total_ttft: float = 0.0  # Time to first token
    total_completion_time: float = 0.0

    # Token counts
    total_prompt_tokens: int = 0
    total_output_tokens: int = 0

    # For computing averages
    _queue_times: List[float] = field(default_factory=list)
    _ttfts: List[float] = field(default_factory=list)
    _completion_times: List[float] = field(default_factory=list)

    def record_request(self, request: Request) -> None:
"""
Record metrics from a finished request.""
if not request.is_finished():
            return

        self.total_requests += 1

        # Categorize by finish reason
        if request.finish_reason == FinishReason.ABORT:
            self.aborted_requests += 1
        elif request.finish_reason == FinishReason.ERROR:
            self.error_requests += 1
        else:
            self.completed_requests += 1

        # Record tokens
        self.total_prompt_tokens += request.num_prompt_tokens
        self.total_output_tokens += request.num_output_tokens

        # Record timing
        if request.time_in_queue is not None:
            self.total_queue_time += request.time_in_queue
            self._queue_times.append(request.time_in_queue)

        if request.time_to_first_token is not None:
            self.total_ttft += request.time_to_first_token
            self._ttfts.append(request.time_to_first_token)

        if request.total_time is not None:
            self.total_completion_time += request.total_time
            self._completion_times.append(request.total_time)


    @property
    def avg_queue_time(self) -> Optional[float]:
"""
Average time spent in queue.""
if not self._queue_times:
            return None
        return sum(self._queue_times) / len(self._queue_times)


    @property
    def avg_ttft(self) -> Optional[float]:
"""
Average time to first token.""
if not self._ttfts:
            return None
        return sum(self._ttfts) / len(self._ttfts)


    @property
    def avg_completion_time(self) -> Optional[float]:
"""
Average total completion time.""
if not self._completion_times:
            return None
        return sum(self._completion_times) / len(self._completion_times)


    @property
    def avg_tokens_per_request(self) -> float:
"""
Average output tokens per completed request.""
if self.completed_requests == 0:
            return 0.0
        return self.total_output_tokens / self.completed_requests


    @property
    def throughput(self) -> Optional[float]:
"""
Tokens per second (based on total completion time).""
if self.total_completion_time == 0:
            return None
        return self.total_output_tokens / self.total_completion_time


    def reset(self) -> None:
"""
Reset all counters.""
self.total_requests = 0
        self.completed_requests = 0
        self.aborted_requests = 0
        self.error_requests = 0
        self.total_queue_time = 0.0
        self.total_ttft = 0.0
        self.total_completion_time = 0.0
        self.total_prompt_tokens = 0
        self.total_output_tokens = 0
        self._queue_times.clear()
        self._ttfts.clear()
        self._completion_times.clear()


    def as_dict(self) -> Dict[str, Any]:
"""
Export metrics as a dictionary.""
return {
            "total_requests": self.total_requests,
            "completed_requests": self.completed_requests,
            "aborted_requests": self.aborted_requests,
            "error_requests": self.error_requests,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_output_tokens": self.total_output_tokens,
            "avg_queue_time": self.avg_queue_time,
            "avg_ttft": self.avg_ttft,
            "avg_completion_time": self.avg_completion_time,
            "avg_tokens_per_request": self.avg_tokens_per_request,
            "throughput": self.throughput,
        }
