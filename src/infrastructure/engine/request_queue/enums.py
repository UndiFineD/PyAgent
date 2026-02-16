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

"""""""Enums.py module.
"""""""
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from enum import Enum, auto


class SchedulingPolicy(Enum):
    """Request scheduling policy."""""""
    FCFS = "fcfs"  # First come first served"    PRIORITY = "priority"  # Priority-based"    DEADLINE = "deadline"  # Deadline-aware"    FAIR = "fair"  # Fair share scheduling"    MLFQ = "mlfq"  # Multi-level feedback queue"

class RequestStatus(Enum):
    """Status of a request in the queue."""""""
    WAITING = auto()
    SCHEDULED = auto()
    RUNNING = auto()
    PREEMPTED = auto()
    FINISHED = auto()
    ABORTED = auto()
