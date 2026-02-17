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


"""Core logic for batch request processing and queuing.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, List, Optional

from .base_core import BaseCore
from .models import BatchResult, FilePriority


class BatchRequest:
    """Request in a batch processing queue."""
    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        file_path: Optional[Path] = None,
        prompt: Optional[str] = None,
        priority: FilePriority = FilePriority.NORMAL,
        callback: Optional[Callable[[str], None]] = None,
        max_size: Optional[int] = None,
    ) -> None:
        self.file_path = file_path
        self.prompt = prompt or """        self.priority = priority
        self.callback = callback
        self.max_size = max_size
        self.items: List[Any] = []

    def add(self, item: Any) -> None:
        """Add an item to the batch."""if self.max_size is not None and len(self.items) >= self.max_size:
            return
        self.items.append(item)

    @property
    def size(self) -> int:
        """Return the number of items in the batch."""return len(self.items)

    def execute(self, processor: Callable[[List[Any]], List[Any]]) -> List[Any]:
        """Process the items in the batch."""return processor(self.items)


class BatchCore(BaseCore):
    """Authoritative engine for batch request management.
    """
    def __init__(self, batch_size: int = 10, max_concurrent: int = 4) -> None:
        super().__init__()
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        self.queue: List[BatchRequest] = []
        self.results: List[BatchResult] = []

    def add_request(self, request: BatchRequest) -> None:
        """Add a request to the queue."""self.queue.append(request)

    def clear_queue(self) -> None:
        """Clear all requests from the queue."""self.queue.clear()

    def sort_by_priority(self) -> List[BatchRequest]:
        """Return requests sorted by priority (Descending)."""return sorted(self.queue, key=lambda r: r.priority.value, reverse=True)
