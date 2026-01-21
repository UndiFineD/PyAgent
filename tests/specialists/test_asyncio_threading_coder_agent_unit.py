import unittest
from src.logic.agents.specialized.asyncio_threading_coder_agent import (
    AsyncioThreadingCoderAgent,
)
from src.core.base.version import VERSION

__version__ = VERSION


class TestAsyncioThreadingCoderAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = AsyncioThreadingCoderAgent("dummy_path.py")

    def test_initialization(self) -> None:
        self.assertIsNotNone(self.agent)
        self.assertIn("AsyncioThreadingCoderAgent", self.agent.__class__.__name__)


if __name__ == "__main__":
    unittest.main()
