import unittest
from src.logic.agents.specialized.asynciothreadingCoderAgent import asynciothreadingCoderAgent
from src.core.base.version import VERSION
__version__ = VERSION




class TestasynciothreadingCoderAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = asynciothreadingCoderAgent("dummy_path.py")



    def test_initialization(self) -> None:
        self.assertIsNotNone(self.agent)
        self.assertIn("asynciothreadingCoderAgent", self.agent.__class__.__name__)


if __name__ == "__main__":
    unittest.main()
