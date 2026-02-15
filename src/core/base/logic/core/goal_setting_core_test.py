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
Tests for Goal Setting and Iterative Refinement Core
"""

import pytest
import asyncio

from src.core.base.logic.core.goal_setting_core import (
    GoalSettingCore,
    GoalStatus,
    GoalPriority,
)


class TestGoalSettingCore:
    """Test suite for goal setting core."""

    def test_goal_creation(self):
        """Test goal creation and validation."""
        core = GoalSettingCore()

        goal = asyncio.run(core.create_goal(
            goal_id="test_goal",
            description="Test goal description",
            criteria=["simple", "tested", "handles edge cases"],
            priority=GoalPriority.HIGH,
            max_iterations=3
        ))

        assert goal.id == "test_goal"
        assert goal.description == "Test goal description"
        assert goal.criteria == ["simple", "tested", "handles edge cases"]
        assert goal.priority == GoalPriority.HIGH
        assert goal.max_iterations == 3
        assert goal.status == GoalStatus.PENDING
        assert goal.current_iteration == 0

    def test_goal_evaluation_default(self):
        """Test default content evaluation."""
        core = GoalSettingCore()

        # Test content that meets criteria
        evaluation = asyncio.run(core.evaluate_content(
            content="This is a simple tested function that handles edge cases",
            criteria=["simple", "tested", "handles edge cases"]
        ))

        assert evaluation["goals_met"] is True
        assert "All criteria met" in evaluation["feedback"]

        # Test content that doesn't meet criteria
        evaluation = asyncio.run(core.evaluate_content(
            content="This is a complex function",
            criteria=["simple", "tested", "handles edge cases"]
        ))

        assert evaluation["goals_met"] is False
        assert "Missing requirement" in evaluation["feedback"]

    def test_goal_refinement_default(self):
        """Test default content refinement."""
        core = GoalSettingCore()

        refined = asyncio.run(core.refine_content(
            content="Original content",
            feedback="Missing requirement: tested",
            criteria=["simple", "tested"]
        ))

        assert "Original content" in refined
        assert "[Refined:" in refined
        # Should not contain the actual criteria to avoid false positives in evaluation
        assert "Missing requirement: tested" not in refined

    @pytest.mark.asyncio
    async def test_iterative_refinement_achievement(self):
        """Test iterative refinement that achieves goals."""
        goal_core = GoalSettingCore()
        try:
            # Create goal
            await goal_core.create_goal(
                goal_id="iterative_goal",
                description="Achieve iterative refinement",
                criteria=["contains success"],
                max_iterations=3
            )

            # Mock evaluation function that succeeds on second try
            async def mock_evaluate(content, criteria):
                if "success" in content:
                    return {
                        "goals_met": True,
                        "feedback": "All criteria met",
                        "confidence_score": 1.0
                    }
                else:
                    return {
                        "goals_met": False,
                        "feedback": "Missing requirement: contains success",
                        "confidence_score": 0.5
                    }

            # Mock refinement function that adds "success"
            async def mock_refine(content, feedback, criteria):
                return content + " success"

            goal_core.register_evaluation_function("mock", mock_evaluate)
            goal_core.register_refinement_function("mock", mock_refine)

            # Execute iteration
            final_goal = await goal_core.iterate_goal("iterative_goal", "Initial content", "mock")

            assert final_goal.status == GoalStatus.ACHIEVED
            assert final_goal.current_iteration == 2  # Should succeed on second iteration
            assert len(final_goal.evaluation_history) == 2
        finally:
            await goal_core.cleanup()

    @pytest.mark.asyncio
    async def test_iterative_refinement_max_iterations(self):
        """Test iterative refinement that hits max iterations."""
        goal_core = GoalSettingCore()
        try:
            # Create goal that will never succeed
            await goal_core.create_goal(
                goal_id="max_iter_goal",
                description="Test max iterations",
                criteria=["xyz_unlikely_word"],
                max_iterations=2
            )

            # Execute iteration with content that won't meet criteria
            final_goal = await goal_core.iterate_goal("max_iter_goal", "Content without the unlikely word")

            assert final_goal.status == GoalStatus.MAX_ITERATIONS_REACHED
            assert final_goal.current_iteration == 2
            assert len(final_goal.evaluation_history) == 2
        finally:
            await goal_core.cleanup()

    @pytest.mark.asyncio
    async def test_goal_status_tracking(self):
        """Test goal status tracking."""
        goal_core = GoalSettingCore()
        try:
            # Create goal
            goal = await goal_core.create_goal("status_goal", "Status test", ["test"])

            # Check initial status
            status = await goal_core.get_goal_status("status_goal")
            assert status.status == GoalStatus.PENDING

            # List active goals
            active = await goal_core.list_active_goals()
            assert len(active) == 1
            assert active[0].id == "status_goal"

            # Complete goal
            goal.status = GoalStatus.ACHIEVED
            goal_core.completed_goals["status_goal"] = goal
            del goal_core.active_goals["status_goal"]

            # Check completed goals
            completed = await goal_core.list_completed_goals()
            assert len(completed) == 1
            assert completed[0].status == GoalStatus.ACHIEVED

            # List active should be empty
            active = await goal_core.list_active_goals()
            assert len(active) == 0
        finally:
            await goal_core.cleanup()
