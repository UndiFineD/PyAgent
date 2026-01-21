import unittest
import os
from src.logic.agents.specialized.quantumscaling_coder_agent import quantumscalingCoderAgent
from src.core.base.version import VERSION
__version__ = VERSION

class TestquantumscalingCoderAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = quantumscalingCoderAgent("dummy_path.py")

    def test_initialization(self) -> None:
        self.assertIsNotNone(self.agent)
        self.assertIn("quantumscalingCoderAgent", self.agent.__class__.__name__)

if __name__ == "__main__":
    unittest.main()