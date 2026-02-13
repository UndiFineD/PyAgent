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
Self Evolution Mixin - Automatic workflow optimization for PyAgent orchestrators

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
Used as a mixin for orchestrator/agent classes that implement execute_with_pattern(context, pattern_name, **kwargs). Instantiate or mix into an agent class, optionally call enable_evolution(False) to disable, and use execute_with_evolution(context, pattern_name, **kwargs) in place of direct execution to get automatic iterative workflow improvements.

WHAT IT DOES:
Implements tracking and lightweight evolutionary optimization around workflow execution: records initial run metrics, decides whether evolution is warranted, attempts a bounded number of evolution iterations, records history and metrics, and returns the best-observed result. Provides configuration hooks (enable_evolution, set_evolution_params) and dataclasses (EvolutionMetrics, EvolutionHistory) to store performance, improvements, and lessons learned.

WHAT IT SHOULD DO BETTER:
- Provide typed return and error contracts for execute_with_evolution to make integration safer (e.g., a Result dataclass and explicit error handling instead of raw Dicts).
- Persist evolution history to durable storage (StateTransaction or rust_core) and expose retrieval/query APIs to analyze long-term trends.
- Use pluggable evolution strategies and validators (strategy pattern) rather than a single internal _evolve_workflow implementation, and add async concurrency controls, timeouts, and resource safeguards for evolved executions.

FILE CONTENT SUMMARY:
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

"""Self-evolution mixin for PyAgent orchestrators."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from src.core.base.common.models.communication_models import CascadeContext, WorkState


@dataclass
class EvolutionMetrics:
    """Metrics for tracking workflow performance."""

    execution_time: float = 0.0
    success_rate: float = 0.0
    quality_score: float = 0.0
    error_count: int = 0
    improvement_iterations: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class EvolutionHistory:
    """History of workflow evolution attempts."""

    original_workflow: Dict[str, Any]
    evolved_workflows: List[Dict[str, Any]] = field(default_factory=list)
    performance_history: List[EvolutionMetrics] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)


class SelfEvolutionMixin:
    """
    Mixin that enables self-evolving capabilities for PyAgent orchestrators.

    This mixin implements automatic workflow optimization based on execution
    feedback, inspired by EvoAgentX's self-evolution algorithms.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize self-evolution capabilities."""
        super().__init__(**kwargs)
        self._evolution_history: Dict[str, EvolutionHistory] = {}
        self._evolution_enabled: bool = True
        self._max_evolution_iterations: int = 3
        self._improvement_threshold: float = 0.1  # 10% improvement required

    def enable_evolution(self, enabled: bool = True) -> None:
        """Enable or disable self-evolution."""
        self._evolution_enabled = enabled

    def set_evolution_params(self, max_iterations: int = 3, improvement_threshold: float = 0.1) -> None:
        """Set evolution parameters."""
        self._max_evolution_iterations = max_iterations
        self._improvement_threshold = improvement_threshold

    async def execute_with_evolution(
        self,
        context: CascadeContext,
        pattern_name: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Execute a workflow with self-evolution capabilities.

        This method executes a workflow and automatically improves it based on
        performance feedback if evolution is enabled.
        """
        if not self._evolution_enabled:
            # Fall back to regular execution
            return await self.execute_with_pattern(context, pattern_name, **kwargs)

        workflow_id = context.task_id

        # Execute initial workflow
        initial_result = await self.execute_with_pattern(context, pattern_name, **kwargs)

        # Track initial performance
        initial_metrics = self._calculate_metrics(initial_result)
        self._record_evolution_step(workflow_id, initial_result, initial_metrics)

        # Check if evolution is needed
        if not self._should_evolve(initial_metrics):
            return initial_result

        # Perform evolution iterations
        best_result = initial_result
        best_metrics = initial_metrics

        for iteration in range(self._max_evolution_iterations):
            # Generate improved workflow
            evolved_workflow = await self._evolve_workflow(
                workflow_id, best_result, best_metrics, iteration
            )

            if evolved_workflow:
                # Execute evolved workflow
                evolved_result = await self._execute_evolved_workflow(
                    evolved_workflow, context, pattern_name, **kwargs
                )

                evolved_metrics = self._calculate_metrics(evolved_result)

                # Record evolution step
                self._record_evolution_step(workflow_id, evolved_result, evolved_metrics)

                # Check if this is better
                if self._is_improved(best_metrics, evolved_metrics):
                    best_result = evolved_result
                    best_metrics = evolved_metrics
                else:
                    # No improvement, stop evolving
                    break

        return best_result

    def _calculate_metrics(self, r
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from src.core.base.common.models.communication_models import CascadeContext, WorkState


@dataclass
class EvolutionMetrics:
    """Metrics for tracking workflow performance."""

    execution_time: float = 0.0
    success_rate: float = 0.0
    quality_score: float = 0.0
    error_count: int = 0
    improvement_iterations: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class EvolutionHistory:
    """History of workflow evolution attempts."""

    original_workflow: Dict[str, Any]
    evolved_workflows: List[Dict[str, Any]] = field(default_factory=list)
    performance_history: List[EvolutionMetrics] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)


class SelfEvolutionMixin:
    """
    Mixin that enables self-evolving capabilities for PyAgent orchestrators.

    This mixin implements automatic workflow optimization based on execution
    feedback, inspired by EvoAgentX's self-evolution algorithms.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize self-evolution capabilities."""
        super().__init__(**kwargs)
        self._evolution_history: Dict[str, EvolutionHistory] = {}
        self._evolution_enabled: bool = True
        self._max_evolution_iterations: int = 3
        self._improvement_threshold: float = 0.1  # 10% improvement required

    def enable_evolution(self, enabled: bool = True) -> None:
        """Enable or disable self-evolution."""
        self._evolution_enabled = enabled

    def set_evolution_params(self, max_iterations: int = 3, improvement_threshold: float = 0.1) -> None:
        """Set evolution parameters."""
        self._max_evolution_iterations = max_iterations
        self._improvement_threshold = improvement_threshold

    async def execute_with_evolution(
        self,
        context: CascadeContext,
        pattern_name: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Execute a workflow with self-evolution capabilities.

        This method executes a workflow and automatically improves it based on
        performance feedback if evolution is enabled.
        """
        if not self._evolution_enabled:
            # Fall back to regular execution
            return await self.execute_with_pattern(context, pattern_name, **kwargs)

        workflow_id = context.task_id

        # Execute initial workflow
        initial_result = await self.execute_with_pattern(context, pattern_name, **kwargs)

        # Track initial performance
        initial_metrics = self._calculate_metrics(initial_result)
        self._record_evolution_step(workflow_id, initial_result, initial_metrics)

        # Check if evolution is needed
        if not self._should_evolve(initial_metrics):
            return initial_result

        # Perform evolution iterations
        best_result = initial_result
        best_metrics = initial_metrics

        for iteration in range(self._max_evolution_iterations):
            # Generate improved workflow
            evolved_workflow = await self._evolve_workflow(
                workflow_id, best_result, best_metrics, iteration
            )

            if evolved_workflow:
                # Execute evolved workflow
                evolved_result = await self._execute_evolved_workflow(
                    evolved_workflow, context, pattern_name, **kwargs
                )

                evolved_metrics = self._calculate_metrics(evolved_result)

                # Record evolution step
                self._record_evolution_step(workflow_id, evolved_result, evolved_metrics)

                # Check if this is better
                if self._is_improved(best_metrics, evolved_metrics):
                    best_result = evolved_result
                    best_metrics = evolved_metrics
                else:
                    # No improvement, stop evolving
                    break

        return best_result

    def _calculate_metrics(self, result: Dict[str, Any]) -> EvolutionMetrics:
        """Calculate performance metrics from execution result."""
        metrics = EvolutionMetrics()

        # Extract metrics from result
        if "final_score" in result:
            metrics.quality_score = result["final_score"]

        if "results" in result and isinstance(result["results"], list):
            total_attempts = len(result["results"])
            successful_attempts = sum(1 for r in result["results"] if r.get("completed", False))
            metrics.success_rate = successful_attempts / total_attempts if total_attempts > 0 else 0.0

        # Calculate execution time (simplified - would need actual timing)
        metrics.execution_time = result.get("execution_time", 0.0)

        # Count errors
        if "results" in result and isinstance(result["results"], list):
            metrics.error_count = sum(1 for r in result["results"] if not r.get("completed", False))

        return metrics

    def _should_evolve(self, metrics: EvolutionMetrics) -> bool:
        """Determine if workflow should be evolved based on metrics."""
        # Evolve if success rate is below threshold or quality score is low
        return metrics.success_rate < 0.8 or metrics.quality_score < 0.7

    async def _evolve_workflow(
        self,
        workflow_id: str,
        current_result: Dict[str, Any],
        current_metrics: EvolutionMetrics,
        iteration: int
    ) -> Optional[Dict[str, Any]]:
        """
        Generate an evolved version of the workflow.

        This method analyzes the current workflow performance and suggests
        improvements based on common evolution patterns.
        """
        evolution_suggestions = self._analyze_workflow_issues(current_result, current_metrics)

        if not evolution_suggestions:
            return None

        # Apply evolution suggestions to create new workflow configuration
        evolved_config = self._apply_evolution_suggestions(
            current_result, evolution_suggestions, iteration
        )

        return evolved_config

    def _analyze_workflow_issues(
        self,
        result: Dict[str, Any],
        metrics: EvolutionMetrics
    ) -> List[str]:
        """Analyze workflow execution to identify improvement opportunities."""
        suggestions = []

        # Analyze success rate
        if metrics.success_rate < 0.8:
            suggestions.append("improve_agent_selection")
            suggestions.append("add_retry_logic")

        # Analyze quality score
        if metrics.quality_score < 0.7:
            suggestions.append("enhance_prompt_quality")
            suggestions.append("add_validation_steps")

        # Analyze errors
        if metrics.error_count > 0:
            suggestions.append("add_error_handling")
            suggestions.append("improve_context_passing")

        # Analyze execution time
        if metrics.execution_time > 60.0:  # More than 1 minute
            suggestions.append("optimize_parallel_execution")
            suggestions.append("reduce_agent_count")

        return suggestions

    def _apply_evolution_suggestions(
        self,
        current_result: Dict[str, Any],
        suggestions: List[str],
        iteration: int
    ) -> Dict[str, Any]:
        """Apply evolution suggestions to create improved workflow."""
        evolved_config = current_result.copy()

        for suggestion in suggestions:
            if suggestion == "improve_agent_selection":
                # Suggest better agent combinations
                evolved_config["agent_improvements"] = evolved_config.get("agent_improvements", [])
                evolved_config["agent_improvements"].append("use_specialized_agents")

            elif suggestion == "add_retry_logic":
                # Add retry mechanisms
                evolved_config["retry_enabled"] = True
                evolved_config["max_retries"] = min(iteration + 2, 5)

            elif suggestion == "enhance_prompt_quality":
                # Improve prompt engineering
                evolved_config["prompt_enhancements"] = evolved_config.get("prompt_enhancements", [])
                evolved_config["prompt_enhancements"].append("add_context_examples")

            elif suggestion == "add_validation_steps":
                # Add validation phases
                evolved_config["validation_enabled"] = True

            elif suggestion == "add_error_handling":
                # Improve error handling
                evolved_config["error_handling"] = "comprehensive"

            elif suggestion == "optimize_parallel_execution":
                # Optimize for parallelism
                evolved_config["parallel_execution"] = True

        evolved_config["evolution_iteration"] = iteration + 1
        return evolved_config

    async def _execute_evolved_workflow(
        self,
        evolved_config: Dict[str, Any],
        context: CascadeContext,
        pattern_name: Optional[str],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute an evolved workflow configuration."""
        # Apply evolved configuration to execution context
        evolved_context = context.next_level(child_task_id=f"evolved_{context.task_id}")

        # Create work state for evolved execution
        work_state = WorkState()
        work_state.update("evolution_config", evolved_config)

        # Execute with evolved configuration (pass work_state in kwargs if needed)
        kwargs["work_state"] = work_state
        result = await self.execute_with_pattern(evolved_context, pattern_name, **kwargs)

        # Mark as evolved result
        result["evolved"] = True
        result["evolution_config"] = evolved_config

        return result

    def _is_improved(self, old_metrics: EvolutionMetrics, new_metrics: EvolutionMetrics) -> bool:
        """Check if new metrics represent an improvement."""
        # Calculate composite improvement score
        old_score = (
            old_metrics.success_rate * 0.4 +
            old_metrics.quality_score * 0.4 +
            (1.0 - min(old_metrics.execution_time / 300.0, 1.0)) * 0.2
        )

        new_score = (
            new_metrics.success_rate * 0.4 +
            new_metrics.quality_score * 0.4 +
            (1.0 - min(new_metrics.execution_time / 300.0, 1.0)) * 0.2
        )

        improvement = (new_score - old_score) / old_score if old_score > 0 else 0
        return improvement >= self._improvement_threshold

    def _record_evolution_step(
        self,
        workflow_id: str,
        result: Dict[str, Any],
        metrics: EvolutionMetrics
    ) -> None:
        """Record an evolution step in history."""
        if workflow_id not in self._evolution_history:
            self._evolution_history[workflow_id] = EvolutionHistory(
                original_workflow=result
            )

        history = self._evolution_history[workflow_id]
        history.evolved_workflows.append(result)
        history.performance_history.append(metrics)

        # Extract lessons learned
        lessons = self._extract_lessons(result, metrics)
        history.lessons_learned.extend(lessons)

    def _extract_lessons(self, result: Dict[str, Any], metrics: EvolutionMetrics) -> List[str]:
        """Extract lessons learned from workflow execution."""
        lessons = []

        if metrics.success_rate > 0.9:
            lessons.append("High success rate indicates good agent selection")

        if metrics.quality_score > 0.8:
            lessons.append("Strong quality score suggests effective collaboration patterns")

        if metrics.error_count == 0:
            lessons.append("Zero errors indicate robust error handling")

        if metrics.execution_time < 30.0:
            lessons.append("Fast execution suggests efficient workflow design")

        return lessons

    def get_evolution_history(self, workflow_id: str) -> Optional[EvolutionHistory]:
        """Get evolution history for a workflow."""
        return self._evolution_history.get(workflow_id)

    def get_evolution_insights(self, workflow_id: str) -> Dict[str, Any]:
        """Get insights from evolution history."""
        history = self.get_evolution_history(workflow_id)
        if not history:
            return {}

        insights = {
            "total_evolutions": len(history.evolved_workflows),
            "best_performance": max(
                history.performance_history,
                key=lambda m: m.quality_score
            ) if history.performance_history else None,
            "lessons_learned": history.lessons_learned,
            "improvement_trend": self._calculate_improvement_trend(history.performance_history)
        }

        return insights

    def _calculate_improvement_trend(self, metrics_history: List[EvolutionMetrics]) -> str:
        """Calculate the trend of performance improvement."""
        if len(metrics_history) < 2:
            return "insufficient_data"

        # Compare first and last metrics
        first = metrics_history[0]
        last = metrics_history[-1]

        first_score = first.success_rate * 0.5 + first.quality_score * 0.5
        last_score = last.success_rate * 0.5 + last.quality_score * 0.5

        if last_score > first_score * 1.1:  # 10% improvement
            return "improving"
        elif last_score < first_score * 0.9:  # 10% decline
            return "declining"
        else:
            return "stable"
