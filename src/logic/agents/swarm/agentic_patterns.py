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

"""Sequential agent orchestration pattern."""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field

from src.core.base.common.models.communication_models import CascadeContext, WorkState
from src.logic.agents.swarm.orchestrator_work_pattern_mixin import OrchestratorWorkPatternMixin

logger = logging.getLogger(__name__)


@dataclass
class SequentialAgentConfig:
    """Configuration for sequential agent execution."""

    name: str
    description: str = ""
    sub_agents: List[Dict[str, Any]] = field(default_factory=list)
    max_retries: int = 3
    continue_on_failure: bool = False
    output_key: Optional[str] = None


class SequentialAgentPattern:
    """
    Sequential agent execution pattern.

    This pattern executes agents in sequence, where each agent's output
    can be used as input for subsequent agents. Inspired by agentic design
    patterns from ADK (Agentic Design Patterns).
    """

    def __init__(self, orchestrator: OrchestratorWorkPatternMixin):
        """Initialize the sequential agent pattern."""
        self.orchestrator = orchestrator

    async def execute_sequential(
        self,
        context: CascadeContext,
        config: SequentialAgentConfig,
        initial_input: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute agents in sequence.

        Args:
            context: Cascade context for execution
            config: Sequential agent configuration
            initial_input: Initial input for the first agent
            **kwargs: Additional execution parameters

        Returns:
            Dict containing execution results
        """
        logger.info(f"Starting sequential execution for {config.name}")

        # Initialize execution state
        execution_state = WorkState()
        execution_state.update("input", initial_input)
        execution_state.update("results", {})

        results = []
        current_input = initial_input

        for i, agent_config in enumerate(config.sub_agents):
            agent_name = agent_config.get("name", f"agent_{i}")
            logger.info(f"Executing agent {i+1}/{len(config.sub_agents)}: {agent_name}")

            try:
                # Create child context for this agent
                agent_context = context.next_level(
                    child_task_id=f"{context.task_id}_seq_{i}",
                    agent_id=agent_name
                )

                # Execute the agent
                agent_result = await self._execute_single_agent(
                    agent_context,
                    agent_config,
                    current_input,
                    execution_state,
                    **kwargs
                )

                results.append({
                    "agent": agent_name,
                    "success": True,
                    "result": agent_result,
                    "sequence_index": i
                })

                # Update execution state with this agent's output
                output_key = agent_config.get("output_key", f"agent_{i}_output")
                execution_state.update(output_key, agent_result)
                execution_state.results[output_key] = agent_result

                # Prepare input for next agent
                current_input = self._prepare_next_input(
                    current_input, agent_result, agent_config
                )

            except Exception as e:
                logger.error(f"Agent {agent_name} failed: {e}")

                results.append({
                    "agent": agent_name,
                    "success": False,
                    "error": str(e),
                    "sequence_index": i
                })

                if not config.continue_on_failure:
                    logger.error(f"Stopping sequential execution due to failure in {agent_name}")
                    break

                # Continue with previous input for next agent
                continue

        # Prepare final result
        final_result = {
            "pattern": "sequential",
            "config": {
                "name": config.name,
                "description": config.description,
                "total_agents": len(config.sub_agents)
            },
            "execution": {
                "total_executed": len(results),
                "successful": sum(1 for r in results if r["success"]),
                "failed": sum(1 for r in results if not r["success"])
            },
            "results": results,
            "final_state": execution_state.results,
            "final_input": current_input
        }

        # Store final output if specified
        if config.output_key:
            final_result[config.output_key] = current_input

        logger.info(f"Completed sequential execution for {config.name}: "
                   f"{final_result['execution']['successful']}/{final_result['execution']['total_executed']} successful")

        return final_result

    async def _execute_single_agent(
        self,
        context: CascadeContext,
        agent_config: Dict[str, Any],
        input_data: Dict[str, Any],
        execution_state: WorkState,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a single agent in the sequence.

        Args:
            context: Agent execution context
            agent_config: Configuration for this agent
            input_data: Input data for the agent
            execution_state: Current execution state
            **kwargs: Additional parameters

        Returns:
            Agent execution result
        """
        agent_type = agent_config.get("type", "pattern")
        agent_name = agent_config.get("name", "unnamed_agent")

        if agent_type == "pattern":
            # Execute using work pattern
            pattern_name = agent_config.get("pattern", "peer")
            pattern_result = await self.orchestrator.execute_with_pattern(
                context, pattern_name, **input_data, **kwargs
            )
            return pattern_result

        elif agent_type == "direct":
            # Direct agent execution (placeholder for future implementation)
            # This would execute a specific agent directly
            return {
                "agent_type": "direct",
                "agent_name": agent_name,
                "input": input_data,
                "output": f"Direct execution result for {agent_name}"
            }

        elif agent_type == "custom":
            # Custom agent logic
            custom_logic = agent_config.get("logic")
            if custom_logic and callable(custom_logic):
                return await custom_logic(context, input_data, execution_state, **kwargs)
            else:
                raise ValueError(f"No custom logic provided for agent {agent_name}")

        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

    def _prepare_next_input(
        self,
        current_input: Dict[str, Any],
        agent_result: Dict[str, Any],
        agent_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare input for the next agent in sequence.

        Args:
            current_input: Current input data
            agent_result: Result from the current agent
            agent_config: Configuration of the current agent

        Returns:
            Input data for the next agent
        """
        # Default behavior: merge agent result with current input
        next_input = current_input.copy()

        # Add agent result
        output_key = agent_config.get("output_key", "agent_output")
        next_input[output_key] = agent_result

        # Add all execution state data
        if isinstance(agent_result, dict) and "final_state" in agent_result:
            next_input.update(agent_result["final_state"])

        return next_input


class ParallelAgentPattern:
    """
    Parallel agent execution pattern.

    This pattern executes multiple agents concurrently and combines their results.
    Inspired by agentic design patterns from ADK.
    """

    def __init__(self, orchestrator: OrchestratorWorkPatternMixin):
        """Initialize the parallel agent pattern."""
        self.orchestrator = orchestrator

    async def execute_parallel(
        self,
        context: CascadeContext,
        agent_configs: List[Dict[str, Any]],
        input_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute multiple agents in parallel.

        Args:
            context: Cascade context for execution
            agent_configs: List of agent configurations
            input_data: Input data for all agents
            **kwargs: Additional execution parameters

        Returns:
            Dict containing combined execution results
        """
        logger.info(f"Starting parallel execution of {len(agent_configs)} agents")

        # Create tasks for parallel execution
        tasks = []
        for i, agent_config in enumerate(agent_configs):
            agent_name = agent_config.get("name", f"agent_{i}")
            agent_context = context.next_level(
                child_task_id=f"{context.task_id}_par_{i}",
                agent_id=agent_name
            )

            task = self._execute_single_agent(
                agent_context, agent_config, input_data, **kwargs
            )
            tasks.append(task)

        # Execute all agents concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        processed_results = []
        successful = 0
        failed = 0

        for i, result in enumerate(results):
            agent_config = agent_configs[i]
            agent_name = agent_config.get("name", f"agent_{i}")

            if isinstance(result, Exception):
                logger.error(f"Agent {agent_name} failed with exception: {result}")
                processed_results.append({
                    "agent": agent_name,
                    "success": False,
                    "error": str(result),
                    "parallel_index": i
                })
                failed += 1
            else:
                processed_results.append({
                    "agent": agent_name,
                    "success": True,
                    "result": result,
                    "parallel_index": i
                })
                successful += 1

        # Combine results
        combined_result = {
            "pattern": "parallel",
            "execution": {
                "total_agents": len(agent_configs),
                "successful": successful,
                "failed": failed
            },
            "results": processed_results,
            "combined_output": self._combine_parallel_results(processed_results)
        }

        logger.info(f"Completed parallel execution: {successful}/{len(agent_configs)} successful")
        return combined_result

    async def _execute_single_agent(
        self,
        context: CascadeContext,
        agent_config: Dict[str, Any],
        input_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a single agent (same logic as sequential pattern)."""
        sequential_pattern = SequentialAgentPattern(self.orchestrator)
        return await sequential_pattern._execute_single_agent(
            context, agent_config, input_data, WorkState(), **kwargs
        )

    def _combine_parallel_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine results from parallel agent execution.

        Args:
            results: List of individual agent results

        Returns:
            Combined result dictionary
        """
        combined = {}

        # Collect all successful results
        successful_results = [r for r in results if r["success"]]

        if not successful_results:
            return {"error": "No successful results from parallel execution"}

        # Combine by agent names
        for result in successful_results:
            agent_name = result["agent"]
            combined[agent_name] = result["result"]

        # Add summary
        combined["_summary"] = {
            "total_agents": len(results),
            "successful_agents": len(successful_results),
            "agent_names": [r["agent"] for r in successful_results]
        }

        return combined
