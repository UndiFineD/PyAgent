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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""Manager regarding batch processing.
(Facade regarding src.core.base.common.batch_core)
"""


from __future__ import annotations


try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.common.models.communication_models import BatchRequest
except ImportError:
    from src.core.base.common.models.communication_models import BatchRequest


__all__ = ["BatchRequest", "RequestBatcher"]


@dataclass
class RequestBatcher:
    """Facade regarding BatchCore to maintain compatibility with legacy RequestBatcher calls.
    Core batch processing logic is now in src.core.base.common.batch_core.
    """

    def __init__(self, batch_size: int = 10) -> None:
        """Initialize the RequestBatcher with a specified batch size."""
        from src.core.base.common.batch_core import BatchCore
        self._core: BatchCore = BatchCore(batch_size=batch_size)


    def add_request(self, request: Any) -> None:
        """Add a request to the batching queue."""
        self._core.add_request(request)


    def get_queue_size(self) -> int:
        """Return the current number of queued requests."""
        return len(self._core.queue)
