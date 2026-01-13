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

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .TestStatus import TestStatus
from dataclasses import dataclass, field
from typing import Optional
import time

__version__ = VERSION

@dataclass
class TestResult:
    __test__ = False
    """Result of a test execution.

    Attributes:
        test_name: Name of the test.
        status: Test status.
        duration_ms: Test duration.
        error_message: Error message if failed.
        assertions_count: Number of assertions.
        timestamp: When test was run.
    """

    test_name: str
    status: TestStatus
    duration_ms: float = 0.0
    error_message: str | None = None
    assertions_count: int = 0
    timestamp: float = field(default_factory=time.time)