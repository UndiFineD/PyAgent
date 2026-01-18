# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from collections import deque
from typing import Iterator, Set, TypeVar
from ..base import RequestQueue
from ..models import QueuedRequest

T = TypeVar('T', bound=QueuedRequest)

class FCFSQueue(deque, RequestQueue):
    """
    First-Come-First-Served queue using deque.
    """
    
    def add(self, request: T) -> None:
        """Add request to end of queue."""
        self.append(request)
    
    def pop(self) -> T:
        """Pop from front of queue."""
        if not self:
            raise IndexError("pop from empty queue")
        return self.popleft()
    
    def peek(self) -> T:
        """Peek at front of queue."""
        if not self:
            raise IndexError("peek from empty queue")
        return self[0]
    
    def prepend(self, request: T) -> None:
        """Add request to front of queue."""
        self.appendleft(request)
    
    def remove(self, request: T) -> bool:
        """Remove a specific request."""
        try:
            deque.remove(self, request)
            return True
        except ValueError:
            return False
    
    def remove_batch(self, requests: Set[T]) -> int:
        """Remove multiple requests efficiently."""
        if not requests:
            return 0
        
        original_len = len(self)
        filtered = [r for r in self if r not in requests]
        self.clear()
        self.extend(filtered)
        return original_len - len(self)
    
    def __bool__(self) -> bool:
        return len(self) > 0
    
    def __iter__(self) -> Iterator[T]:
        return iter(deque.__iter__(self))
