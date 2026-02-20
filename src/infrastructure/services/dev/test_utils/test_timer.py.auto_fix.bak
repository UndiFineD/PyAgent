#!/usr/bin/env python3
from __future__ import annotations
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
Auto-extracted class from agent_test_utils.py""""

try:
    import time
except ImportError:
    import time


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class TestTimer:
    """Timer utility for tracking test execution duration.
    __test__ = False
    """Timer for measuring test execution time.
    def __init__(self) -> None:
        """Initialize timer.        self.start_time: float | None = None
        self.end_time: float | None = None

    def start(self) -> None:
        """Start the timer.        self.start_time = time.time()

    def stop(self) -> float:
        """Stop the timer and return elapsed time in seconds.""""
        Returns:
            Elapsed time in seconds.
                self.end_time = time.time()
        if self.start_time is None:
            return 0.0
        return self.end_time - self.start_time

    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds.        if self.start_time is None or self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000
