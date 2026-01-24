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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Output object pooling for the model runner."""

import queue
import threading
from typing import Callable, Generic, Optional, TypeVar

T = TypeVar("T")


class AsyncGPUPoolingModelRunnerOutput(Generic[T]):
    """
    Pooled async output container.

    vLLM Pattern: AsyncGPUPoolingModelRunnerOutput

    Reduces allocation overhead by reusing output objects.
    """

    def __init__(self, pool_size: int = 100):
        self._pool: queue.Queue[T] = queue.Queue(maxsize=pool_size)
        self._factory: Optional[Callable[[], T]] = None
        self._allocated = 0
        self._reused = 0
        self._lock = threading.Lock()

    def set_factory(self, factory: Callable[[], T]) -> None:
        """Set factory for creating new output objects."""
        self._factory = factory

    def acquire(self) -> Optional[T]:
        """Acquire output object from pool."""
        try:
            obj = self._pool.get_nowait()
            with self._lock:
                self._reused += 1
            return obj
        except queue.Empty:
            if self._factory:
                with self._lock:
                    self._allocated += 1
                return self._factory()
            return None

    def release(self, obj: T) -> None:
        """Return output object to pool."""
        try:
            self._pool.put_nowait(obj)
        except queue.Full:
            pass  # Pool is full, object will be GC'd

    def get_stats(self) -> dict[str, int]:
        """Get pool statistics."""
        with self._lock:
            return {
                "pool_size": self._pool.qsize(),
                "allocated": self._allocated,
                "reused": self._reused,
                "reuse_ratio": self._reused / max(1, self._allocated + self._reused),
            }
