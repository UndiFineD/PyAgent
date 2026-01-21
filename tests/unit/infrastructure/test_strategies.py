"""Unit tests for agent execution strategies (Direct, CoT, Reflexion)."""

import unittest
from unittest.mock import MagicMock, AsyncMock
import os

# Add src to path

from src.core.base.lifecycle.base_agent import BaseAgent
from src.logic.strategies.direct_strategy import DirectStrategy
from src.logic.strategies.chain_of_thought_strategy import ChainOfThoughtStrategy
from src.logic.strategies.reflexion_strategy import ReflexionStrategy


class TestStrategies(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        # Create a dummy file so BaseAgent init doesn't fail
        with open("test_file.txt", "w") as f:
            f.write("Original Content")

        self.agent = BaseAgent("test_file.txt")
        self.agent.previous_content = "Original Content"
        self.agent.run_subagent = AsyncMock(return_value="Improved Content")

        # Disable cache and retries
        self.agent._config.cache_enabled = False
        self.agent._config.retry_count = 0

        # Mock quality check to always pass
        self.agent._score_response_quality = MagicMock(
            return_value=MagicMock(value=100)
        )  # High value

    def tearDown(self) -> None:
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")

    async def test_direct_strategy(self) -> None:
        self.agent.set_strategy(DirectStrategy())
        await self.agent.improve_content("Fix bugs")

        # Check if run_subagent was called once
        self.agent.run_subagent.assert_called_once()
        args = self.agent.run_subagent.call_args
        # args[0] is (description, prompt, original_content)
        # prompt is at index 1
        self.assertIn("Fix bugs", args[0][1])

    async def test_cot_strategy(self) -> None:
        self.agent.set_strategy(ChainOfThoughtStrategy())
        await self.agent.improve_content("Fix bugs")

        # Check if run_subagent was called twice (Reasoning + Implementation)
        self.assertEqual(self.agent.run_subagent.call_count, 2)

        # Check first call (Reasoning)
        args1 = self.agent.run_subagent.call_args_list[0]
        self.assertIn("Think step-by-step", args1[0][1])

        # Check second call (Implementation)
        args2 = self.agent.run_subagent.call_args_list[1]

        self.assertIn("Based on the following reasoning", args2[0][1])

    async def test_reflexion_strategy(self) -> None:
        self.agent.set_strategy(ReflexionStrategy())

        # Mock run_subagent to return different values based on prompt
        async def side_effect(desc, prompt, content) -> str:
            if "Critique" in prompt:
                return "Critique: Good but needs X"
            if "Revise" in prompt:
                return "Revised Content"
            return "Draft Content"

        self.agent.run_subagent = AsyncMock(side_effect=side_effect)

        await self.agent.improve_content("Fix bugs")

        # Should be called 3 times (Draft, Critique, Revise)
        self.assertEqual(self.agent.run_subagent.call_count, 3)


if __name__ == "__main__":
    unittest.main()
