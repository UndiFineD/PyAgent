"""
Integration test for Plugin Sandbox permissions.
Verifies that the PluginManager correctly identifies and eventually (Phase 318) enforces
sandbox permissions.
"""

import unittest
import logging
from pathlib import Path
from src.core.base.logic.managers.plugin_manager import PluginManager

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
            res_src = plugin.run(Path("src\core\base\base_agent.py"), {})
            self.assertTrue(res_src)

            res_temp = plugin.run(Path("temp/test.txt"), {})
            self.assertTrue(res_temp)
        else:
            self.fail("test_sandbox metadata not loaded")

if __name__ == "__main__":
    unittest.main()
