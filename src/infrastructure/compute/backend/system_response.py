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


"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from dataclasses import dataclass

__version__ = VERSION


@dataclass
class SystemResponse:
    """Response from a backend request.

    Attributes:
        content: Response content.
        backend: Backend that provided response.
        latency_ms: Response latency in milliseconds.
        cached: Whether response was from cache.
        request_id: ID of originating request.
        tokens_used: Estimated tokens consumed.
    """

    content: str
    backend: str
    latency_ms: int = 0
    cached: bool = False
    request_id: str | None = None
    tokens_used: int = 0
