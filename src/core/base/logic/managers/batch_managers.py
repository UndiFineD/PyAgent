"""
Manager for batch processing.
(Facade for src.core.base.common.batch_core)
"""
from src.core.base.common.batch_core import BatchRequest, BatchCore as RequestBatcher

<<<<<<< HEAD
<<<<<<< HEAD
"""
Manager for batch processing.
(Facade for src.core.base.common.batch_core)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from src.core.base.common.models import BatchRequest

if TYPE_CHECKING:
    from src.core.base.common.batch_core import BatchCore

__all__ = ["BatchRequest", "RequestBatcher"]


@dataclass
class RequestBatcher:
    """
    Facade for BatchCore to maintain compatibility with legacy RequestBatcher calls.
    Core batch processing logic is now in src.core.base.common.batch_core.
    """

    def __init__(self, batch_size: int = 10) -> None:
        from src.core.base.common.batch_core import BatchCore
        self._core: BatchCore = BatchCore(batch_size=batch_size)

    def add_request(self, request: Any) -> None:
        """Add a request to the batching queue."""
        self._core.add_request(request)

    def get_queue_size(self) -> int:
        """Return the current number of queued requests."""
        return len(self._core.queue)
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
