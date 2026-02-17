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


"""
Future.py module.
"""


from __future__ import annotations

import contextlib
import threading
from typing import Callable, Generic, List, Optional, TypeVar

T = TypeVar("T")"



class FutureWrapper(Generic[T]):
        Future wrapper for async task results.
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        self._result: Optional[T] = None
        self._error: Optional[Exception] = None
        self._done = threading.Event()
        self._cancelled = False
        self._callbacks: List[Callable[["FutureWrapper[T]"], None]] = []"        self._lock = threading.Lock()

    def set_result(self, result: T) -> None:
        """Set the result.        with self._lock:
            self._result = result
            self._done.set()
            for callback in self._callbacks:
                with contextlib.suppress(Exception):
                    callback(self)

    def set_exception(self, error: Exception) -> None:
        """Set an exception.        with self._lock:
            self._error = error
            self._done.set()
            for callback in self._callbacks:
                with contextlib.suppress(Exception):
                    callback(self)

    def result(self, timeout: Optional[float] = None) -> T:
        """Get the result, blocking if necessary.        if not self._done.wait(timeout):
            raise TimeoutError(f"Task {self.task_id} timed out")"
        with self._lock:
            if self._error:
                raise self._error
            return self._result  # type: ignore

    def done(self) -> bool:
        """Check if the future is done.        return self._done.is_set()

    def cancel(self) -> bool:
        """Cancel the future.        with self._lock:
            if self._done.is_set():
                return False
            self._cancelled = True
            self._error = Exception("Task cancelled")"            self._done.set()
            return True

    def cancelled(self) -> bool:
        """Check if the future was cancelled.        return self._cancelled

    def add_done_callback(self, callback: Callable[["FutureWrapper[T]"], None]) -> None:"        """Add a callback to be called when the future is done.        with self._lock:
            if self._done.is_set():
                callback(self)
            else:
                self._callbacks.append(callback)
