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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Agentic Patterns - Sequential Agent Orchestration

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate SequentialAgentPattern with an
  OrchestratorWorkPatternMixin implementation and
  call execute_sequential with a CascadeContext,
  a SequentialAgentConfig, and an initial input
  dict.
- Example:
  config = SequentialAgentConfig(
      name="example",
      sub_agents=[{"name":"step1"}, {"name":"step2"}]
  )
  pattern = SequentialAgentPattern(orchestrator)
  result = await pattern.execute_sequential(
      context, config, {"prompt": "start"}
  )

WHAT IT DOES:
- Orchestrates a list of sub-agents in sequence.
- Passes outputs from one agent as inputs to the next.
- Tracks results in a WorkState and optionally
  continues on failure.
- Creates per-agent child CascadeContext entries.
- Executes agents via an internal
  _execute_single_agent coroutine.
- Records outputs to execution_state.
- Assembles a final result structure describing
  successes and failures.

WHAT IT SHOULD DO BETTER:
- Provide explicit type hints and return schemas for
  agent results and execution_state to improve
  static analysis and downstream consumption.
- Surface retry/backoff behavior and configurable
  timeouts per sub-agent (max_retries exists but
  lacks per-agent control and backoff).
- Improve error reporting by including exception
  types, stack traces (when permitted), and
  structured error codes; add observability hooks
  (metrics, tracing) and better unit-test coverage
  for failure paths and input transformation logic.

FILE CONTENT SUMMARY:
Sequential agent orchestration pattern.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    # Keep the real imports for static type checkers (mypy, IDEs)
    from src.core.base.common.models.communication_models import CascadeContext, WorkState  # type: ignore
else:
    # Runtime fallback stubs to avoid import errors when the package or stubs are not available.
    pass

class CascadeContext:
    """Fallback stub for CascadeContext.

    Lightweight stub used at runtime when real CascadeContext is unavailable;
    preserves a task_id and can create child contexts.
    """
    def __init__(self, *_args, task_id: str = "task", **_kwargs):
        self.task_id = task_id

    def next_level(self, child_task_id: str = ", _agent_id: str = ") -> "CascadeContext":
        """Return a child CascadeContext preserving or overriding task_id."""
        # Simple passthrough stub that preserves a task_id for downstream code that uses it.
        return CascadeContext(task_id=child_task_id or self.task_id)

class WorkState:
    """Fallback stub for WorkState which stores results in a dict."""
    def __init__(self):
        self.results = {}

    def update(self, key, value):
        """Update the internal results mapping."""
        self.results[key] = value

from src.logic.agents.swarm.orchestrator_work_pattern_mixin import OrchestratorWorkPatternMixin

logger = logging.getLogger(__name__)


@dataclass
class SequentialAgentConfig:
    """Configuration for sequential agent execution."""

    name: str
#     description: str =
    sub_agents: List[Dict[str, Any]] = field(default_factory=list)
    max_retries: int = 3
    continue_on_failure: bool = False
    output_key: Optional[str] = None


class SequentialAgentPattern:
    """Sequential agent execution pattern.

    This pattern executes agents in sequence, where each agent's output
    can be used as input for subsequent agents. Inspired by agentic design
    patterns from ADK (Agentic" Design Patterns).
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

        # Initialize execution state safely (WorkState API may vary)
        execution_state = WorkState()
        # Prefer WorkState.update when available; otherwise store data in execution_state.results map
        try:
            execution_state.update("input", initial_input)
        except Exception:
            # Fallback: store the initial input in the results mapping if present or create it
            try:
                if hasattr(execution_state, "results") and isinstance(getattr(execution_state, "results"), dict):
                    execution_state.results["input"] = initial_input
                else:
                    setattr(execution_state, "results", {"input": initial_input})
            except Exception:
                # If all else fails, skip setting to avoid assigning unknown attributes
                pass

        # ensure a results container on execution_state
        try:
            execution_state.update("results", {})
        except Exception:
            if not hasattr(execution_state, "results"):
                setattr(execution_state, "results", {})

        results = []
        current_input = initial_input

        for i, agent_config in enumerate(config.sub_agents):
            agent_name = agent_config.get("name", f"agent_{i}")
            logger.info(f"Executing agent {i+1}/{len(config.sub_agents)}: {agent_name}")

            try:
                # Create child context for this agent
                agent_context = context.next_level(
                    child_task_id=f"{getattr(context, 'task_id', 'task')}_seq_{i}",
                    agent_id=agent_name
                )

                # Execute the agent (delegates to orchestrator if available)
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
                try:
                    execution_state.update(output_key, agent_result)
                except Exception:
                    # ensure results map is present and set there
                    if not hasattr(execution_state, "results"):
                        setattr(execution_state, "results", {})
                    execution_state.results[output_key] = agent_result

                # Prepare input for next agent
                current_input = self._prepare_next_input(
                    current_input, agent_result, agent_config
                )

            except Exception as e:
                logger.exception(f"Agent {agent_name} failed")
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
                "sub_agents_count": len(config.sub_agents),
                "continue_on_failure": config.continue_on_failure,
            },
            "results": results,
            "execution_state": getattr(execution_state, "results", {})
        }

        return final_result

    async def _execute_single_agent(
        self,
        agent_context: CascadeContext,
        agent_config: Dict[str, Any],
        current_input: Dict[str, Any],
        execution_state: WorkState,
        **kwargs
    ) -> Any:
        """
        Execute a single agent using the orchestrator when available, otherwise
        provide a safe fallback result.

        This method intentionally attempts common orchestrator entrypoints and
        falls back to sensible defaults to avoid runtime AttributeError.
        Args:
            agent_context: Cascade context for the agent
            agent_config: Configuration dict for the agent
            current_input: Input data for the agent
            execution_state: Current execution state to allow stateful operations
            **kwargs: Additional parameters that may be needed for execution
        """
        # Try execute_with_pattern first (preferred for work patterns)
        if hasattr(self.orchestrator, 'execute_with_pattern') and callable(getattr(self.orchestrator, 'execute_with_pattern')):
            try:
                pattern_name = agent_config.get("pattern")
                if pattern_name:
                    result = self.orchestrator.execute_with_pattern(
                        agent_context, pattern_name, input_data=current_input, **kwargs
                    )
                    if asyncio.iscoroutine(result):
                        return await result
                    return result
            except Exception:
                logger.exception("Orchestrator execute_with_pattern raised an exception")
                raise

        # Preferred orchestrator method names (try common candidates)
        candidate_methods = ("execute_agent", "run_agent", "execute", "run")
        for method in candidate_methods:
            fn = getattr(self.orchestrator, method, None)
            if callable(fn):
                try:
                    # Assume orchestrator methods are async; await if coroutine
                    result = fn(agent_context, agent_config, current_input, execution_state, **kwargs)
                    if asyncio.iscoroutine(result):
                        return await result
                    return result
                except Exception:
                    logger.exception("Orchestrator method '%s' raised an exception", method)
                    raise

        # If agent_config itself provides a callable payload, try that
        provided_callable = agent_config.get("callable") if isinstance(agent_config, dict) else None
        if callable(provided_callable):
            result = provided_callable(agent_context, agent_config, current_input, execution_state, **kwargs)
            if asyncio.iscoroutine(result):
                return await result
            return result

        # Fallback: return explicit 'output' in agent_config, or echo current_input
        if isinstance(agent_config, dict) and "output" in agent_config:
            return agent_config["output"]

        # Safe default: return current_input unchanged
        return current_input

    def _prepare_next_input(
        self,
        current_input: Dict[str, Any],
        agent_result: Any,
        agent_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare the input for the next agent in the sequence by merging
        dict results or storing non-dict results under an output key.
        """
        # If agent_result is a dict, merge shallowly (agent result wins)
        if isinstance(agent_result, dict):
            merged = {}
            if isinstance(current_input, dict):
                merged.update(current_input)
            merged.update(agent_result)
            return merged

        # Use explicit output_key if provided
        output_key = agent_config.get("output_key") if isinstance(agent_config, dict) else None
        if output_key:
            next_input = {}
            if isinstance(current_input, dict):
                next_input.update(current_input)
            next_input[output_key] = agent_result
            return next_input

        # Otherwise, place under a generic key
        next_input = {}
        if isinstance(current_input, dict):
            next_input.update(current_input)
        next_input["last_output"] = agent_result
        return next_input
