
import unittest
import shutil
import logging
from pathlib import Path
from src.classes.fleet.PluginManager import PluginManager

class TestPluginManager(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.ERROR)
        self.workspace = Path(".").resolve()
        self.plugin_manager = PluginManager(self.workspace)
        
    def test_discovery(self):
        plugins = self.plugin_manager.discover()
        print(f"Discovered plugins: {plugins}")
        # We expect at least the example_math_plugin if it exists
        # or verify the logic runs without crashing
        self.assertIsInstance(plugins, list)
        
    def test_math_plugin_if_exists(self):
        # We created this in a previous turn
        math_plugin_path = self.workspace / "plugins" / "example_math_plugin" / "__init__.py"
        if math_plugin_path.exists():
            print("Found example_math_plugin")
            plugins = self.plugin_manager.discover()
            self.assertIn("example_math_plugin", plugins)
            
if __name__ == '__main__':
    unittest.main()
