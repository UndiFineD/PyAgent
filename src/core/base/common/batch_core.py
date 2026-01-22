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

"""
Core logic for batch request processing and queuing.
"""

from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, List, Optional, Callable
from .base_core import BaseCore
from .models import FilePriority, BatchResult

class BatchRequest:
    """Request in a batch processing queue."""
    def __init__(
        self,
        file_path: Optional[Path] = None,
        prompt: Optional[str] = None,
        priority: FilePriority = FilePriority.NORMAL,
        callback: Optional[Callable[[str], None]] = None,
        max_size: Optional[int] = None,
    ) -> None:
        self.file_path = file_path
        self.prompt = prompt or ""
        self.priority = priority
        self.callback = callback
        self.max_size = max_size
        self.items: List[Any] = []

    def add(self, item: Any) -> None:
        if self.max_size is not None and len(self.items) >= self.max_size:
            return
        self.items.append(item)

    @property
    def size(self) -> int:
        return len(self.items)

    def execute(self, processor: Callable[[List[Any]], List[Any]]) -> List[Any]:
        return processor(self.items)

class BatchCore(BaseCore):
    """
    Authoritative engine for batch request management.
    """
    def __init__(self, batch_size: int = 10, max_concurrent: int = 4) -> None:
        super().__init__()
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        self.queue: List[BatchRequest] = []
        self.results: List[BatchResult] = []

    def add_request(self, request: BatchRequest) -> None:
        self.queue.append(request)

    def clear_queue(self) -> None:
        self.queue.clear()

    def sort_by_priority(self) -> List[BatchRequest]:
        return sorted(self.queue, key=lambda r: r.priority.value, reverse=True)
