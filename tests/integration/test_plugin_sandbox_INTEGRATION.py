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

"""
Integration test for Plugin Sandbox permissions.
Verifies that the PluginManager correctly identifies and eventually (Phase 318) enforces
sandbox permissions.
"""

import unittest
import logging
from pathlib import Path
from src.core.base.managers.PluginManager import PluginManager

class TestPluginSandboxIntegration(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.ERROR)
        self.workspace = Path(".").resolve()
        self.pm = PluginManager(self.workspace)

    def test_sandbox_plugin_discovery_and_execution(self):
        """Verifies that the test_sandbox plugin is discovered and can be loaded."""
        discovered = self.pm.discover()

        # Check if test_sandbox is present
        self.assertIn("test_sandbox", discovered, "test_sandbox plugin not discovered")

        if "test_sandbox" in self.pm.loaded_meta:
            meta = self.pm.loaded_meta["test_sandbox"]
            # verify permissions exist in meta
            permissions = meta.get("permissions", [])
            self.assertIsInstance(permissions, list)

            plugin = self.pm.load_plugin("test_sandbox")
            self.assertIsNotNone(plugin, "Failed to load test_sandbox plugin")

            # Simulated execution
            # Current implementation of test_sandbox just returns True
            res_src = plugin.run(Path("src/core/base/BaseAgent.py"), {})
            self.assertTrue(res_src)

            res_temp = plugin.run(Path("temp/test.txt"), {})
            self.assertTrue(res_temp)
        else:
            self.fail("test_sandbox metadata not loaded")

if __name__ == "__main__":
    unittest.main()
