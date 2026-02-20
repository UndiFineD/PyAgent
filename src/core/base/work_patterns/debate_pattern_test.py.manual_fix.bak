#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Tests for debate work pattern.""
try:

"""
import pytest
except ImportError:
    import pytest

try:
    from unittest.mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock


try:
    from .core.base.common.models.communication_models import CascadeContext
except ImportError:
    from src.core.base.common.models.communication_models import CascadeContext

try:
    from .core.base.work_patterns import DebateWorkPattern
except ImportError:
    from src.core.base.work_patterns import DebateWorkPattern




class MockDebateAgent:
"""
Mock agent for debate testing.""
def __init__(self, agent_id: str, role: str, incentives: str = "Balanced reasoning"):"        self.agent_id = agent_id
        self.role = role
        self.incentives = incentives
        self.system_prompt = f"You are a {role} with incentives: {incentives}"


class TestDebateWorkPattern:
"""
Test the debate work pattern.""
def test_initialization(self):
"""
Test pattern initialization.""
pattern = DebateWorkPattern()
        assert pattern.name == "Debate""        assert pattern.description == "Multi-agent debate pattern""        assert pattern.config.max_rounds == 3
        assert pattern.config.quality_threshold == 0.8

    def test_validate_agents_valid(self):
"""
        Test validating valid debate agents.""
        pattern = DebateWorkPattern()

        agents = [
        MockDebateAgent("agent1", "Advocate"),"            MockDebateAgent("agent2", "Critic")"        ]

        assert pattern.validate_agents(agents) is True

    def test_validate_agents_insufficient_count(self):
"""
        Test validating with insufficient agents.""
        pattern = DebateWorkPattern()

        agents = [MockDebateAgent("agent1", "Advocate")]
        assert pattern.validate_agents(agents) is False

    def test_validate_agents_duplicate_roles(self):
"""
        Test validating agents with duplicate roles.""
        pattern = DebateWorkPattern()

        agents = [
        MockDebateAgent("agent1", "Advocate"),"            MockDebateAgent("agent2", "Advocate")  # Duplicate role"        ]

        assert pattern.validate_agents(agents) is False

    def test_validate_agents_missing_role(self):
"""
        Test validating agents without role attribute.""
        pattern = DebateWorkPattern()

        # Create an agent without role attribute
        agent_without_role = MagicMock()
        del agent_without_role.role  # Ensure no role attribute

        agents = [
        MockDebateAgent("agent1", "Advocate"),"            agent_without_role
        ]

        assert pattern.validate_agents(agents) is False

        @pytest.mark.asyncio
        async def test_execute_debate_success(self):
"""
        Test successful debate execution.""
        advocate = MockDebateAgent("advocate", "Advocate", "Maximize user benefit")"        auditor = MockDebateAgent("auditor", "Auditor", "Minimize risk")"
        pattern = DebateWorkPattern(advocate_agent=advocate, auditor_agent=auditor)

        context = CascadeContext(task_id="test_debate")
        result = await pattern.execute(context)

        assert result["pattern"] == "Debate""        assert "debate_history" in result"        assert "final_decision" in result"        assert result["participants"] == 2"        assert result["rounds_completed"] >= 1
        @pytest.mark.asyncio
        async def test_execute_debate_insufficient_agents(self):
"""
        Test debate execution with insufficient agents.""
        advocate = MockDebateAgent("advocate", "Advocate")
        pattern = DebateWorkPattern(advocate_agent=advocate)  # Only one agent

        context = CascadeContext(task_id="test_debate")
        with pytest.raises(ValueError, match="Debate pattern requires at least 2 agents"):"            await pattern.execute(context)

    def test_check_consensus_high_confidence(self):
"""
        Test consensus detection with high confidence.""
        pattern = DebateWorkPattern()

        round_results = {
        "arguments": ["                {"position": {"confidence": 0.9}},"                {"position": {"confidence": 0.85}}"            ]
        }

        assert pattern._check_consensus(round_results) is True

    def test_check_consensus_low_confidence(self):
"""
        Test consensus detection with low confidence.""
        pattern = DebateWorkPattern()

        round_results = {
        "arguments": ["                {"position": {"confidence": 0.6}},"                {"position": {"confidence": 0.7}}"            ]
        }

        assert pattern._check_consensus(round_results) is False

    def test_check_consensus_insufficient_agents(self):
"""
        Test consensus detection with insufficient agents.""
        pattern = DebateWorkPattern()

        round_results = {
        "arguments": [{"position": {"confidence": 0.9}}]"        }

        assert pattern._check_consensus(round_results) is False

        @pytest.mark.asyncio
        async def test_auto_synthesis(self):
"""
        Test automatic decision synthesis.""
        pattern = DebateWorkPattern()

        debate_history = [{
        "arguments": ["                {
        "role": "Advocate","                    "position": {"confidence": 0.8, "decision": "Implement"}"                },
        {
        "role": "Auditor","                    "position": {"confidence": 0.9, "decision": "Review carefully"}"                }
        ]
        }]

        participants = [
        MockDebateAgent("agent1", "Advocate"),"            MockDebateAgent("agent2", "Auditor")"        ]

        result = await pattern._auto_synthesis(debate_history, participants)

        assert result["method"] == "auto""        assert result["winning_role"] == "Auditor""        assert result["confidence"] == 0.9
        @pytest.mark.asyncio
        async def test_weighted_vote_synthesis(self):
        ""
        Test weighted vote decision synthesis.""
        pattern = DebateWorkPattern()

        debate_history = [{
        "arguments": ["                {"role": "Advocate", "position": {"decision": "Implement"}},"                {"role": "Auditor", "position": {"decision": "Review"}}"            ]
        }]

        participants = [
        MockDebateAgent("agent1", "Advocate"),"            MockDebateAgent("agent2", "Auditor")"        ]

        result = await pattern._weighted_vote_synthesis(debate_history, participants)

        assert result["method"] == "weighted_vote""        assert "votes" in result"        assert result["votes"]["Auditor"] == 1.5  # Higher weight for auditor"        assert result["votes"]["Advocate"] == 1.2  # Higher weight for advocate"