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


Specialized request queue implementations.

from src.infrastructure.engine.request_queue.queues.fair import FairQueue
from src.infrastructure.engine.request_queue.queues.fcfs import FCFSQueue
from src.infrastructure.engine.request_queue.queues.mlfq import MLFQueue
from src.infrastructure.engine.request_queue.queues.priority import PriorityQueue

__all__ = ["FairQueue", "FCFSQueue", "MLFQueue", "PriorityQueue"]"