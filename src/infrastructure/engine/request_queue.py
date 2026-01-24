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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for Request Queue.
Delegates to modularized sub-packages in src/infrastructure/engine/request_queue/.
"""

from __future__ import annotations

from .request_queue import (DeadlineQueue, FairQueue, FCFSQueue, MLFQueue,
                            PriorityQueue, QueuedRequest, RequestPriority,
                            RequestQueue, RequestQueueManager, RequestStatus,
                            SchedulingPolicy, create_request_queue)

__all__ = [
    "SchedulingPolicy",
    "RequestStatus",
    "RequestPriority",
    "QueuedRequest",
    "RequestQueue",
    "FCFSQueue",
    "PriorityQueue",
    "DeadlineQueue",
    "FairQueue",
    "MLFQueue",
    "RequestQueueManager",
    "create_request_queue",
]
