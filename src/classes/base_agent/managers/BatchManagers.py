#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

from __future__ import annotations
import logging
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING
from ..models import FilePriority, BatchResult

# Infrastructure
from src.classes.backend.LocalContextRecorder import LocalContextRecorder

if TYPE_CHECKING:
    from ..agent import BaseAgent

class BatchRequest:
    """Request in a batch processing queue."""

    def __init__(
        self,
        file_path: Optional[Path] = None,
        prompt: Optional[str] = None,
        priority: FilePriority = FilePriority.NORMAL,
        callback: Optional[Callable[[str], None]] = None,
        max_size: Optional[int] = None
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


class RequestBatcher:
    """Batch processor for multiple file requests."""

    def __init__(self, batch_size: int = 10, max_concurrent: int = 4, recorder: Optional[LocalContextRecorder] = None) -> None:
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        self.recorder = recorder
        self.queue: List[BatchRequest] = []
        self.results: List[BatchResult] = []
        logging.debug(f"RequestBatcher initialized with batch_size={batch_size}")

    def add_request(self, request: BatchRequest) -> None:
        self.queue.append(request)

    def add_requests(self, requests: List[BatchRequest]) -> None:
        self.queue.extend(requests)

    def get_queue_size(self) -> int:
        return len(self.queue)

    def clear_queue(self) -> None:
        self.queue.clear()

    def _sort_by_priority(self) -> List[BatchRequest]:
        return sorted(self.queue, key=lambda r: r.priority.value, reverse=True)

    def process_batch(self, agent_factory: Callable[[str], BaseAgent]) -> List[BatchResult]:
        sorted_requests = self._sort_by_priority()
        batch = sorted_requests[:self.batch_size]
        results: List[BatchResult] = []
        
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
                if request.callback: request.callback(content)
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

    def process_all(self, agent_factory: Callable[[str], BaseAgent]) -> List[BatchResult]:
        all_results: List[BatchResult] = []
        while self.queue:
            batch_results = self.process_batch(agent_factory)
            all_results.extend(batch_results)
        return all_results

    def get_stats(self) -> Dict[str, Any]:
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


