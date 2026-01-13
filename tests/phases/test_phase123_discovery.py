import unittest
from src.infrastructure.fleet.FleetManager import FleetManager
from pathlib import Path
import os
import time

class TestPhase123Discovery(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.root)

    def test_discovery_orchestrator_initialization(self) -> None:
        # Accessing it should trigger __init__ and start thread
        discovery = self.fleet.orchestrators.discovery
        self.assertIsNotNone(discovery)
        self.assertTrue(hasattr(discovery, "zeroconf"))
        
    def test_discovery_advertising(self) -> None:
        discovery = self.fleet.orchestrators.discovery
        # Give it a few seconds to start the thread and register
        time.sleep(5)
        self.assertTrue(discovery._is_advertising)
        
    def tearDown(self):
        if hasattr(self.fleet.orchestrators, "discovery"):
            self.fleet.orchestrators.discovery.shutdown()

if __name__ == "__main__":
    unittest.main()
