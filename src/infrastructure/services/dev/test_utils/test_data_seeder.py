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
from src.core.base.version import VERSION
from typing import Any, Dict, List, Optional, Union
import random
import time

__version__ = VERSION

try:
    import numpy as np
except ImportError:
    np = None

class TestDataSeeder:
    __test__ = False
    """Generates reproducible test data with optional seeding."""

    def __init__(self, seed: int | None = None) -> None:
        """Initialize test data seeder.

        Args:
            seed: Random seed for reproducibility.
        """
        self.seed = seed
        # Use an instance RNG to avoid global-random interference across tests.
        self._rng = random.Random(seed)
        if seed is not None and np:
            np.random.seed(seed)

    def generate_metric_data(self, count: int = 10) -> list[dict[str, str | float]]:
        """Generate metric data for testing.

        Args:
            count: Number of metrics to generate.

        Returns:
            List of metric dictionaries.
        """
        return [
            {
                "metric": f"metric_{i}",
                "value": self._rng.uniform(0, 100),
                "timestamp": time.time() + i
            }
            for i in range(count)
        ]

    def generate_test_results(self, count: int = 10, pass_rate: float = 0.8) -> list[dict[str, Any]]:
        """Generate test results for testing.

        Args:
            count: Number of test results to generate.
            pass_rate: Fraction of tests that should pass.

        Returns:
            List of test result dictionaries.
        """
        return [
            {
                "test_name": f"test_{i}",
                "status": "PASSED" if self._rng.random() < pass_rate else "FAILED",
                "duration_ms": self._rng.uniform(10, 5000)
            }
            for i in range(count)
        ]

    def generate_file_content(self, language: str = "python") -> str:
        """Generate sample file content.

        Args:
            language: Programming language ("python", "javascript", etc.).

        Returns:
            Generated file content.
        """
        # Use a deterministic return value based on seed for reproducibility
        func_id = self.seed if self.seed is not None else self._rng.randint(1, 100)
        return_val = self._rng.randint(1, 100)
        if language == "python":
            return f'# Python file\ndef func_{func_id}():\n    return {return_val}\n'
        elif language == "javascript":
            return f'// JavaScript file\nfunction func_{func_id}() {{\n  return {return_val};\n}}\n'
        else:
            return f"// Generic content\nval_{func_id} = {return_val}\n"

    def generate_unique_id(self) -> str:
        """Generate a unique ID.

        Returns:
            Unique ID string.
        """
        return f"id_{int(time.time() * 1000000)}_{random.randint(1000, 9999)}"

    def generate_bulk_data(self, count: int = 10, data_type: str = "python_code") -> list[str]:
        """Generate bulk data.

        Args:
            count: Number of items to generate.
            data_type: Type of data to generate.

        Returns:
            List of generated data items.
        """
        if data_type == "python_code":
            return [f"def func_{i}():\n    return {i}\n" for i in range(count)]
        elif data_type == "ids":
            return [self.generate_unique_id() for _ in range(count)]
        else:
            return [f"item_{i}_{self.generate_unique_id()}" for i in range(count)]