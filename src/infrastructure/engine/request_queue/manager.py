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


"""
Manager.py module.

"""

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

try:
    import threading
except ImportError:
    import threading

try:
    import time
except ImportError:
    import time

try:
    from typing import Any, Dict, Optional
except ImportError:
    from typing import Any, Dict, Optional


try:
    from .enums import RequestStatus, SchedulingPolicy
except ImportError:
    from .enums import RequestStatus, SchedulingPolicy

try:
    from .factory import create_request_queue
except ImportError:
    from .factory import create_request_queue

try:
    from .models import QueuedRequest
except ImportError:
    from .models import QueuedRequest




class RequestQueueManager:
        Manages multiple request queues with different policies.
    
    def __init__(
        self,
        policy: SchedulingPolicy = SchedulingPolicy.FCFS,
        max_queue_size: int = 10000,
    ) -> None:
        self.policy = policy
        self.max_queue_size = max_queue_size
        self._queue = create_request_queue(policy)
        self._lock = threading.Lock()

        # Statistics
        self.total_added = 0
        self.total_popped = 0
        self.total_removed = 0
        self.max_observed_size = 0

    def add(self, request: QueuedRequest) -> bool:
"""
Add request with admission control.        with self._lock:
            if len(self._queue) >= self.max_queue_size:
                return False

            self._queue.add(request)
            self.total_added += 1
            self.max_observed_size = max(self.max_observed_size, len(self._queue))
            return True

    def pop(self) -> Optional[QueuedRequest]:
"""
Pop next request.        with self._lock:
            if not self._queue:
                return None

            request = self._queue.pop()
            request.status = RequestStatus.SCHEDULED
            request.scheduled_time = time.time()
            self.total_popped += 1
            return request

    def peek(self) -> Optional[QueuedRequest]:
"""
Peek at next request.        with self._lock:
            if not self._queue:
                return None
            return self._queue.peek()

    def remove(self, request_id: str) -> bool:
"""
Remove request by ID.        with self._lock:
            for req in self._queue:
                if req.request_id == request_id:
                    if self._queue.remove(req):
                        self.total_removed += 1
                        return True
            return False

    def __len__(self) -> int:
        return len(self._queue)

    def get_stats(self) -> Dict[str, Any]:
"""
Get queue statistics.        with self._lock:
            return {
                "policy": self.policy.value,"                "current_size": len(self._queue),"                "max_size": self.max_queue_size,"                "total_added": self.total_added,"                "total_popped": self.total_popped,"                "total_removed": self.total_removed,"                "max_observed_size": self.max_observed_size,"            }

"""
