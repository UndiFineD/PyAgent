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

"""
Goal Setting and Iterative Refinement Core

Implements goal-driven iterative improvement patterns for self-correcting agents.
Based on agentic design patterns with goal evaluation, iterative refinement, and
self-correction reasoning techniques.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.core.base.common.base_core import BaseCore


class GoalStatus(str, Enum):
    """Goal achievement status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    FAILED = "failed"
    MAX_ITERATIONS_REACHED = "max_iterations_reached"


class GoalPriority(str, Enum):
    """Goal priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Goal:
    """Represents a goal with evaluation criteria."""
    id: str
    description: str
    criteria: List[str]  # List of criteria that must be met
    priority: GoalPriority = GoalPriority.MEDIUM
    max_iterations: int = 5
    current_iteration: int = 0
    status: GoalStatus = GoalStatus.PENDING
    evaluation_history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def is_achieved(self) -> bool:
        """Check if goal is achieved based on latest evaluation."""
        if not self.evaluation_history:
            return False
        return self.evaluation_history[-1].get("goals_met", False)

    def should_continue_iteration(self) -> bool:
        """Check if we should continue iterating."""
        return (self.current_iteration < self.max_iterations and
                self.status not in [GoalStatus.ACHIEVED, GoalStatus.FAILED])


@dataclass
class IterationResult:
    """Result of a single iteration."""
    iteration: int
    content: str
    evaluation: Dict[str, Any]
    feedback: str
    goals_met: bool
    timestamp: datetime = field(default_factory=datetime.now)


class GoalSettingCore(BaseCore):
    """
    Core for goal-driven iterative refinement and self-correction.

    Implements patterns from agentic design patterns including:
    - Goal setting with evaluation criteria
    - Iterative refinement with feedback loops
    - Self-correction reasoning
    - Goal achievement tracking
    """

    def __init__(self):
        super().__init__()
        self.active_goals: Dict[str, Goal] = {}
        self.completed_goals: Dict[str, Goal] = {}
        self.evaluation_functions: Dict[str, Callable] = {}
        self.refinement_functions: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)

    async def create_goal(
        self,
        goal_id: str,
        description: str,
        criteria: List[str],
        priority: GoalPriority = GoalPriority.MEDIUM,
        max_iterations: int = 5
    ) -> Goal:
        """
        Create a new goal with evaluation criteria.

        Args:
            goal_id: Unique identifier for the goal
            description: Human-readable description
            criteria: List of criteria that must be met
            priority: Priority level
            max_iterations: Maximum number of refinement iterations

        Returns:
            Created Goal object
        """
        goal = Goal(
            id=goal_id,
            description=description,
            criteria=criteria,
            priority=priority,
            max_iterations=max_iterations
        )

        self.active_goals[goal_id] = goal
        self.logger.info(f"Created goal {goal_id}: {description}")
        return goal

    def register_evaluation_function(self, goal_type: str, func: Callable):
        """
        Register a custom evaluation function for a goal type.

        Args:
            goal_type: Type of goal this function evaluates
            func: Function that takes content and criteria, returns evaluation dict
        """
        self.evaluation_functions[goal_type] = func

    def register_refinement_function(self, goal_type: str, func: Callable):
        """
        Register a custom refinement function for a goal type.

        Args:
            goal_type: Type of goal this function refines
            func: Function that takes content, feedback, and criteria, returns refined content
        """
        self.refinement_functions[goal_type] = func

    async def evaluate_content(
        self,
        content: str,
        criteria: List[str],
        goal_type: str = "default"
    ) -> Dict[str, Any]:
        """
        Evaluate content against goal criteria.

        Args:
            content: Content to evaluate
            criteria: List of criteria to check
            goal_type: Type of goal for custom evaluation

        Returns:
            Evaluation results with goals_met boolean and detailed feedback
        """
        if goal_type in self.evaluation_functions:
            return await self.evaluation_functions[goal_type](content, criteria)

        # Default evaluation logic
        evaluation = {
            "goals_met": True,
            "criteria_results": {},
            "feedback": "",
            "confidence_score": 0.0
        }

        feedback_parts = []

        for criterion in criteria:
            # Simple keyword-based evaluation (can be enhanced with LLM)
            if any(keyword.lower() in content.lower() for keyword in criterion.split()):
                evaluation["criteria_results"][criterion] = True
            else:
                evaluation["criteria_results"][criterion] = False
                evaluation["goals_met"] = False
                feedback_parts.append(f"Missing requirement: {criterion}")

        evaluation["feedback"] = "; ".join(feedback_parts) if feedback_parts else "All criteria met"
        evaluation["confidence_score"] = 1.0 if evaluation["goals_met"] else 0.5

        return evaluation

    async def refine_content(
        self,
        content: str,
        feedback: str,
        criteria: List[str],
        goal_type: str = "default"
    ) -> str:
        """
        Refine content based on feedback and criteria.

        Args:
            content: Original content
            feedback: Feedback from evaluation
            criteria: Goal criteria
            goal_type: Type of goal for custom refinement

        Returns:
            Refined content
        """
        if goal_type in self.refinement_functions:
            return await self.refinement_functions[goal_type](content, feedback, criteria)

        # Default refinement logic - provide generic improvement suggestions
        # In a real implementation, this would use an LLM to generate meaningful improvements
        # without revealing the exact criteria that need to be met
        refinement_note = "\n\n[Refined: Improved content structure and clarity based on evaluation feedback]"
        return f"{content}{refinement_note}"

    async def iterate_goal(
        self,
        goal_id: str,
        initial_content: str,
        goal_type: str = "default"
    ) -> Goal:
        """
        Execute iterative refinement for a goal.

        Args:
            goal_id: ID of the goal to iterate
            initial_content: Starting content
            goal_type: Type of goal for custom functions

        Returns:
            Updated Goal object
        """
        if goal_id not in self.active_goals:
            raise ValueError(f"Goal {goal_id} not found")

        goal = self.active_goals[goal_id]
        goal.status = GoalStatus.IN_PROGRESS
        current_content = initial_content

        while goal.should_continue_iteration():
            goal.current_iteration += 1
            self.logger.info(f"Goal {goal_id} iteration {goal.current_iteration}")

            # Evaluate current content
            evaluation = await self.evaluate_content(current_content, goal.criteria, goal_type)

            # Record evaluation
            iteration_result = IterationResult(
                iteration=goal.current_iteration,
                content=current_content,
                evaluation=evaluation,
                feedback=evaluation.get("feedback", ""),
                goals_met=evaluation.get("goals_met", False)
            )

            goal.evaluation_history.append({
                "iteration": iteration_result.iteration,
                "content": iteration_result.content,
                "evaluation": iteration_result.evaluation,
                "goals_met": iteration_result.goals_met,
                "timestamp": iteration_result.timestamp.isoformat()
            })

            # Check if goals are met
            if evaluation.get("goals_met", False):
                goal.status = GoalStatus.ACHIEVED
                goal.completed_at = datetime.now()
                self.logger.info(f"Goal {goal_id} achieved in {goal.current_iteration} iterations")
                break

            # Check if max iterations reached
            if goal.current_iteration >= goal.max_iterations:
                goal.status = GoalStatus.MAX_ITERATIONS_REACHED
                self.logger.warning(f"Goal {goal_id} reached max iterations without achievement")
                break

            # Refine content for next iteration
            current_content = await self.refine_content(
                current_content,
                evaluation.get("feedback", ""),
                goal.criteria,
                goal_type
            )

        # Move to completed goals
        if goal.status in [GoalStatus.ACHIEVED, GoalStatus.FAILED, GoalStatus.MAX_ITERATIONS_REACHED]:
            self.completed_goals[goal_id] = goal
            del self.active_goals[goal_id]

        return goal

    async def get_goal_status(self, goal_id: str) -> Optional[Goal]:
        """Get the current status of a goal."""
        if goal_id in self.active_goals:
            return self.active_goals[goal_id]
        return self.completed_goals.get(goal_id)

    async def list_active_goals(self) -> List[Goal]:
        """List all active goals."""
        return list(self.active_goals.values())

    async def list_completed_goals(self) -> List[Goal]:
        """List all completed goals."""
        return list(self.completed_goals.values())

    async def cleanup(self):
        """Cleanup resources."""
        self.active_goals.clear()
        self.completed_goals.clear()
        self.evaluation_functions.clear()
        self.refinement_functions.clear()
