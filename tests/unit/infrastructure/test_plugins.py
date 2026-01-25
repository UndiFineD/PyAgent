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

"""Unit tests for PluginManager logic."""

from typing import List
import unittest
import logging
from pathlib import Path
import pytest

try:
    from src.core.base.common.base_managers import PluginManager
except ImportError:
    PluginManager = None  # type: ignore

pytestmark = pytest.mark.skipif(
    PluginManager is None,
    reason="PluginManager not available in BaseManagers"
)


@pytest.mark.skipif(PluginManager is None, reason="PluginManager not available")
class TestPluginManager(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.ERROR)
        self.workspace: Path = Path(".").resolve()
        self.plugin_manager = PluginManager(self.workspace)

    def test_discovery(self) -> None:
        plugins: List[str] = self.plugin_manager.discover()
        print(f"Discovered plugins: {plugins}")
        # We expect at least the example_math_plugin if it exists
        # or verify the logic runs without crashing

        self.assertIsInstance(plugins, list)

    def test_math_plugin_if_exists(self) -> None:
        # We created this in a previous turn
        math_plugin_path: Path = (
            self.workspace / "plugins" / "example_math_plugin" / "__init__.py"
        )

        if math_plugin_path.exists():
            print("Found example_math_plugin")
            plugins: List[str] = self.plugin_manager.discover()
            self.assertIn("example_math_plugin", plugins)


if __name__ == "__main__":
    unittest.main()
