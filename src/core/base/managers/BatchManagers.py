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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import time
from pathlib import Path
from typing import Any, TYPE_CHECKING
from collections.abc import Callable
from src.core.base.models import FilePriority, BatchResult

__version__ = VERSION

if TYPE_CHECKING:
    from ..agent import BaseAgent
    from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder







class BatchRequest:
    """Request in a batch processing queue."""

    def __init__(
        self,
        file_path: Path | None = None,
        prompt: str | None = None,
        priority: FilePriority = FilePriority.NORMAL,










        callback: Callable[[str], None] | None = None,
        max_size: int | None = None
    ) -> None:



        self.file_path = file_path
        self.prompt = prompt or ""
        self.priority = priority
        self.callback = callback





        self.max_size = max_size
        self.items: list[Any] = []

    def add(self, item: Any) -> None:
        if self.max_size is not None and len(self.items) >= self.max_size:

            return
        self.items.append(item)

    @property
    def size(self) -> int:




        return len(self.items)

    def execute(self, processor: Callable[[list[Any]], list[Any]]) -> list[Any]:
        return processor(self.items)





class RequestBatcher:
    """Batch processor for multiple file requests."""

    def __init__(self, batch_size: int = 10, max_concurrent: int = 4, recorder: LocalContextRecorder | None = None) -> None:
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        self.recorder = recorder
        self.queue: list[BatchRequest] = []
        self.results: list[BatchResult] = []
        logging.debug(f"RequestBatcher initialized with batch_size={batch_size}")

    def add_request(self, request: BatchRequest) -> None:
        self.queue.append(request)

    def add_requests(self, requests: list[BatchRequest]) -> None:
        self.queue.extend(requests)

    def get_queue_size(self) -> int:
        return len(self.queue)

    def clear_queue(self) -> None:
        self.queue.clear()

    def _sort_by_priority(self) -> list[BatchRequest]:
        return sorted(self.queue, key=lambda r: r.priority.value, reverse=True)

    def process_batch(self, agent_factory: Callable[[str], BaseAgent]) -> list[BatchResult]:
        sorted_requests = self._sort_by_priority()
        batch = sorted_requests[:self.batch_size]
        results: list[BatchResult] = []

        if self.recorder:
            self.recorder.record_lesson("batch_processing_start", {"batch_size": len(batch)})

        for request in batch:
            start_time = time.time()
            try:
                agent = agent_factory(str(request.file_path))
                agent.read_previous_content()
                content = agent.improve_content(request.prompt)
                result = BatchResult(
                    file_path=request.file_path,
                    success=True,
                    content=content,
                    processing_time=time.time() - start_time
                )
                if request.callback:
                    request.callback(content)
            except Exception as e:
                result = BatchResult(
                    file_path=request.file_path,
                    success=False,
                    error=str(e),
                    processing_time=time.time() - start_time
                )
            results.append(result)
            self.queue.remove(request)
        self.results.extend(results)
        return results

    def process_all(self, agent_factory: Callable[[str], BaseAgent]) -> list[BatchResult]:
        all_results: list[BatchResult] = []
        while self.queue:
            batch_results = self.process_batch(agent_factory)
            all_results.extend(batch_results)
        return all_results

    def get_stats(self) -> dict[str, Any]:
        if not self.results:
            return {"processed": 0, "success_rate": 0.0, "avg_time": 0.0}
        successful = sum(1 for r in self.results if r.success)
        total_time = sum(r.processing_time for r in self.results)
        return {
            "processed": len(self.results),
            "successful": successful,
            "failed": len(self.results) - successful,
            "success_rate": successful / len(self.results),
            "avg_time": total_time / len(self.results),
            "total_time": total_time,
        }
