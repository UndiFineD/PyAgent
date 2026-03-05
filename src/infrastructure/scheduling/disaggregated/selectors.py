# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import random
from abc import ABC, abstractmethod
from typing import List, Optional
from .config import InstanceInfo, ScheduledRequest


class InstanceSelector(ABC):
    """Abstract base for instance selection strategies."""

    @abstractmethod
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        """Select an instance for the request."""
        ...


class RoundRobinSelector(InstanceSelector):
    """Round-robin instance selection."""

    def __init__(self):
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
    """Select least loaded instance."""

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
    """Random instance selection."""

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
    """Hash-based consistent instance selection."""

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
