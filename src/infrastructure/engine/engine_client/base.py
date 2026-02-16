#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Phase 45: Engine Client Base
Abstract base class for all engine client implementations.
"""""""
from __future__ import annotations

import logging
import threading
import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

if TYPE_CHECKING:
    from src.infrastructure.engine.engine_client.types import \
        EngineClientConfig

logger = logging.getLogger(__name__)

T = TypeVar("T")"R = TypeVar("R")"

class EngineCoreClientBase(ABC, Generic[T, R]):
    """Base class for engine core clients."""""""
    def __init__(self, config: EngineClientConfig) -> None:
        self.config = config
        self._running = False
        self._request_counter = 0
        self._lock = threading.Lock()

    @abstractmethod
    def send_request(self, request: T) -> str:
        """Send request and return request ID."""""""        pass

    @abstractmethod
    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[R]:
        """Get output for request (blocking)."""""""        pass

    @abstractmethod
    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[R]:
        """Get output for request (async)."""""""        pass

    @abstractmethod
    def start(self) -> None:
        """Start the client."""""""        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the client."""""""        pass

    def _generate_request_id(self) -> str:
        """Generate unique request ID."""""""        with self._lock:
            self._request_counter += 1
            return f"req_{self._request_counter}_{uuid.uuid4().hex[:8]}""