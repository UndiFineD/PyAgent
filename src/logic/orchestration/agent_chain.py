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


"""Auto-extracted class from agent.py"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.logic.orchestration.agent_chain_step import AgentChainStep

__version__ = VERSION


class AgentChain:
    """Chain multiple agents for sequential execution.

    Allows output of one agent to be used as input to the next.

    Example:
        chain=AgentChain()
        chain.add_step("coder", output_transform=extract_code)
        chain.add_step("tests", input_transform=prepare_for_tests)
        results=chain.execute(initial_input)
    """

    def __init__(self, name: str = "default_chain") -> None:
        """Initialize agent chain.

        Args:
            name: Chain name for identification.
        """
        self.name = name
        self._steps: list[AgentChainStep] = []
        self._results: list[dict[str, Any]] = []

    def add_step(
        self,
        agent_name: str,
        input_transform: Callable[[Any], Any] | None = None,
        output_transform: Callable[[Any], Any] | None = None,
        condition: Callable[[Any], bool] | None = None,
    ) -> AgentChain:
        """Add a step to the chain.

        Args:
            agent_name: Name of agent to execute.
            input_transform: Transform input before agent.
            output_transform: Transform output after agent.
            condition: Condition to check before execution.

        Returns:
            Self for chaining.
        """
        step = AgentChainStep(
            agent_name=agent_name,
            input_transform=input_transform,
            output_transform=output_transform,
            condition=condition,
        )
        self._steps.append(step)
        return self

    def execute(self, initial_input: Any, agent_executor: Callable[[str, Any], Any]) -> list[dict[str, Any]]:
        """Execute the chain.

        Args:
            initial_input: Input to first agent.
            agent_executor: Function to execute an agent.

        Returns:
            List of results from each step.
        """
        self._results = []
        current_input = initial_input

        for step in self._steps:
            if not step.enabled:
                continue

            # Check condition
            if step.condition and not step.condition(current_input):
                self._results.append(
                    {
                        "agent": step.agent_name,
                        "skipped": True,
                        "reason": "condition not met",
                    }
                )
                continue

            # Transform input
            if step.input_transform:
                current_input = step.input_transform(current_input)

            # Execute agent
            try:
                output = agent_executor(step.agent_name, current_input)

                # Transform output
                if step.output_transform:
                    output = step.output_transform(output)

                self._results.append(
                    {
                        "agent": step.agent_name,
                        "success": True,
                        "output": output,
                    }
                )

                current_input = output

            except Exception as e:
                self._results.append(
                    {
                        "agent": step.agent_name,
                        "success": False,
                        "error": str(e),
                    }
                )
                break

        return self._results

    def get_results(self) -> list[dict[str, Any]]:
        """Get results from last execution."""
        return self._results
