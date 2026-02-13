#!/usr/bin/env python3
# Refactored by copilot-placeholder
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


"""
MockCore for a community-submitted plugin.
Demonstrates the 'Core/Shell' pattern for cross-language compatibility.
"""

from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class MockCore:
    """Pure logic for the MockPlugin."""

    def __init__(self, multiplier: float = 1.0) -> None:
        self.multiplier: float = multiplier
        self.processed_count: int = 0

    def calculate_dummy_value(self, input_val: float) -> float:
        """Example pure calculation."""
        self.processed_count += 1
        return input_val * self.multiplier + (self.processed_count * 0.1)

    def format_mock_response(self, original_text: str) -> str:
        """Example pure string manipulation."""
        return f"[MOCK-CORE-V1] {original_text[::-1]}"

    def get_metadata(self) -> dict[str, Any]:
        return {
            "version": "1.0.0",
            "author": "CommunityMember",
            "calls_made": self.processed_count,
        }
