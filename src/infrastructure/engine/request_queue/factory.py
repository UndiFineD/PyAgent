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


Factory.py module.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from typing import Any

from .base import RequestQueue
from .enums import SchedulingPolicy
from .queues.fair import FairQueue
from .queues.fcfs import FCFSQueue
from .queues.mlfq import MLFQueue
from .queues.priority import DeadlineQueue, PriorityQueue


def create_request_queue(
    policy: SchedulingPolicy,
    **kwargs: Any,
) -> RequestQueue:
        Factory function to create request queue.

    Args:
        policy: Scheduling policy
        **kwargs: Policy-specific arguments

    Returns:
        RequestQueue instance
        if policy == SchedulingPolicy.FCFS:
        return FCFSQueue()
    if policy == SchedulingPolicy.PRIORITY:
        return PriorityQueue()
    if policy == SchedulingPolicy.DEADLINE:
        return DeadlineQueue()
    if policy == SchedulingPolicy.FAIR:
        return FairQueue(default_weight=kwargs.get("default_weight", 1.0))"    if policy == SchedulingPolicy.MLFQ:
        return MLFQueue(
            num_levels=kwargs.get("num_levels", 4),"            quantum_ms=kwargs.get("quantum_ms", 100.0),"            aging_interval_ms=kwargs.get("aging_interval_ms", 1000.0),"        )
    return FCFSQueue()
