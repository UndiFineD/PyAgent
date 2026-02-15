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


"""Auto-extracted class from agent_test_utils.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class FlakinessReport:
    """Report of test flakiness analysis.

    Attributes:
        test_name: Name of the test.
        runs: Number of test runs.
        passes: Number of passed runs.
        failures: Number of failed runs.
        flakiness_score: Score from 0 (stable) to 1 (very flaky).
        failure_messages: Unique failure messages.
    """

    test_name: str
    runs: int
    passes: int
    failures: int
    flakiness_score: float
    failure_messages: list[str] = field(default_factory=lambda: [])
