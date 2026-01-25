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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import TypeVar

from src.core.base.lifecycle.version import VERSION

T = TypeVar("T")

__version__ = VERSION


class RetryHelper:
    """Simple retry helper for flaky operations."""

    def __init__(self, max_retries: int = 3, delay_seconds: float = 0.0) -> None:
        self.max_retries = int(max_retries)
        self.delay_seconds = float(delay_seconds)

    def retry(self, fn: Callable[[], T]) -> T:
        last_exc: BaseException | None = None
        for attempt in range(self.max_retries):
            try:
                return fn()
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                # noqa: BLE001
                last_exc = exc
                if attempt == self.max_retries - 1:
                    raise
                if self.delay_seconds > 0:
                    threading.Event().wait(self.delay_seconds)
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("RetryHelper failed without exception")
