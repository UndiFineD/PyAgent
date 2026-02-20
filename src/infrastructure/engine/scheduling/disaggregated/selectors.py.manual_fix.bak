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
Selectors.py module.

"""

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

try:
    import random
except ImportError:
    import random

try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from typing import List, Optional
except ImportError:
    from typing import List, Optional


try:
    from .config import InstanceInfo, ScheduledRequest
except ImportError:
    from .config import InstanceInfo, ScheduledRequest




class InstanceSelector(ABC):
"""
Abstract base for instance selection strategies.
    @abstractmethod
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
"""
Select an instance for the request.        raise NotImplementedError



class RoundRobinSelector(InstanceSelector):
"""
Round-robin instance selection.
    def __init__(self) -> None:
        self._counter = 0

    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        if not instances:
            return None

        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            return None

        idx = self._counter % len(healthy)
        self._counter += 1
        return healthy[idx]



class LeastLoadedSelector(InstanceSelector):
"""
Select least loaded instance.
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            return None

        return min(healthy, key=lambda i: i.load_score)



class RandomSelector(InstanceSelector):
"""
Random instance selection.
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            return None

        return random.choice(healthy)



class HashSelector(InstanceSelector):
"""
Hash-based consistent instance selection.
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            return None

        # Hash request ID to select instance
        hash_val = hash(request.request_id)
        idx = hash_val % len(healthy)
        return healthy[idx]
