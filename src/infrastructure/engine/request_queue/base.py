# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from abc import ABC, abstractmethod
from typing import Generic, Iterator, TypeVar
from .models import QueuedRequest

T = TypeVar('T', bound=QueuedRequest)

class RequestQueue(ABC, Generic[T]):
    """Abstract base class for request queues."""

    @abstractmethod
    def add(self, request: T) -> None:
        """Add a request to the queue."""
        pass

    @abstractmethod
    def pop(self) -> T:
        """Pop the next request from the queue."""
        pass

    @abstractmethod
    def peek(self) -> T:
        """Peek at the next request without removing."""
        pass

    @abstractmethod
    def prepend(self, request: T) -> None:
        """Add request to front (for preemption)."""
        pass

    @abstractmethod
    def remove(self, request: T) -> bool:
        """Remove a specific request."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __bool__(self) -> bool:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass
