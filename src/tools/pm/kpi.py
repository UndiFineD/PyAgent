#!/usr/bin/env python3
"""KPI computation functions for PyAgent."""
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

from typing import Any, Sequence


def compute_throughput(completed: Sequence[Any], period: Sequence[Any]) -> int:
    # `period` parameter is reserved for future use; currently ignored
    """Return a simple throughput metric (items per unit period).

    For the sake of the initial test we simply return the number of
    completed items; later versions may divide by time or apply weighting.
    """
    return len(completed)
