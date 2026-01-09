#!/usr/bin/env python3

"""
MockCore for a community-submitted plugin.
Demonstrates the 'Core/Shell' pattern for cross-language compatibility.
"""

import time
from typing import Dict, Any, List

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

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "version": "1.0.0",
            "author": "CommunityMember",
            "calls_made": self.processed_count
        }
