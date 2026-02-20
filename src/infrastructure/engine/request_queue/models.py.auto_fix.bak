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


Models.py module.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

try:
    import time
except ImportError:
    import time

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Any, Optional
except ImportError:
    from typing import Any, Optional


try:
    from .enums import RequestStatus
except ImportError:
    from .enums import RequestStatus



@dataclass
class RequestPriority:
        Composite priority for request scheduling.

    Lower values = higher priority (processed first).
    
    priority: int = 0  # User-specified priority (lower = higher)
    arrival_time: float = field(default_factory=time.time)
    deadline: Optional[float] = None
    boost_factor: float = 1.0  # Dynamic priority boost

    def __lt__(self, other: "RequestPriority") -> bool:"        """Compare for heap ordering.        # Priority first (lower is better)
        if self.priority != other.priority:
            return self.priority < other.priority
        # Then arrival time (earlier is better)
        return self.arrival_time < other.arrival_time

    def effective_priority(self) -> float:
        """Get effective priority with boost applied.        return self.priority / self.boost_factor


@dataclass
class QueuedRequest:
        Request wrapper for queue management.

    Contains request data and queue metadata.
    
    request_id: str
    data: Any
    priority: RequestPriority = field(default_factory=RequestPriority)
    status: RequestStatus = RequestStatus.WAITING

    # Queue tracking
    queue_time: float = field(default_factory=time.time)
    scheduled_time: Optional[float] = None

    # Client/tenant for fair scheduling
    client_id: Optional[str] = None

    # Token counts for scheduling decisions
    num_prompt_tokens: int = 0
    max_tokens: int = 256

    def __lt__(self, other: "QueuedRequest") -> bool:"        """Compare for heap ordering.        return self.priority < other.priority

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QueuedRequest):
            return False
        return self.request_id == other.request_id

    def __hash__(self) -> int:
        return hash(self.request_id)

    @property
    def wait_time(self) -> float:
        """Time spent waiting in queue.        return time.time() - self.queue_time

    @property
    def is_deadline_critical(self) -> bool:
        """Check if deadline is approaching.        if self.priority.deadline is None:
            return False
        return time.time() > self.priority.deadline * 0.9
