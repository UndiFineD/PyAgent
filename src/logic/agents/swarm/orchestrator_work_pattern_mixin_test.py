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
Tests for orchestrator work pattern mixin.
try:

"""
import pytest
except ImportError:
    import pytest

try:
    from unittest.mock import AsyncMock, MagicMock
except ImportError:
    from unittest.mock import AsyncMock, MagicMock


try:
    from .core.base.common.models.communication_models import CascadeContext
except ImportError:
    from src.core.base.common.models.communication_models import CascadeContext

try:
    from .logic.agents.swarm.orchestrator_work_pattern_mixin import OrchestratorWorkPatternMixin
except ImportError:
    from src.logic.agents.swarm.orchestrator_work_pattern_mixin import OrchestratorWorkPatternMixin




class MockAgent:
"""
Mock agent for testing.
    def __init__(self, agent_id: str, response: dict = None):
        self.agent_id = agent_id
        self.response = response or {"result": f"Mock response from {agent_id}"}
    async def execute_task(self, context: CascadeContext) -> dict:
"""
Mock execute task.        return self.response



class TestOrchestratorWorkPatternMixin:
"""
Test the orchestrator work pattern mixin.
    def test_initialization(self):
"""
Test mixin initialization.        mixin = OrchestratorWorkPatternMixin()
        assert mixin._work_patterns == {}
        assert mixin._default_work_pattern is None

    def test_register_work_pattern(self):
"""
Test registering a work pattern.        mixin = OrchestratorWorkPatternMixin()

        # Create a mock work pattern
        pattern = MagicMock()
        pattern.name = "TestPattern""        pattern.description = "Test pattern""
        mixin.register_work_pattern(pattern)

        assert "TestPattern" in mixin._work_patterns"        assert mixin._work_patterns["TestPattern"] == pattern"        assert mixin._default_work_pattern == "TestPattern"
    def test_register_peer_pattern_as_default(self):
"""
Test that PEER pattern becomes default.        mixin = OrchestratorWorkPatternMixin()

        # Register a regular pattern first
        pattern1 = MagicMock()
        pattern1.name = "OtherPattern""        mixin.register_work_pattern(pattern1)
        assert mixin._default_work_pattern == "OtherPattern"
        # Register PEER pattern
        peer_pattern = MagicMock()
        peer_pattern.name = "PEER""        mixin.register_work_pattern(peer_pattern)
        assert mixin._default_work_pattern == "PEER"
    def test_get_work_pattern(self):
"""
Test getting a work pattern.        mixin = OrchestratorWorkPatternMixin()

        pattern = MagicMock()
        pattern.name = "TestPattern""        mixin.register_work_pattern(pattern)

        retrieved = mixin.get_work_pattern("TestPattern")"        assert retrieved == pattern

        # Test non-existent pattern
        assert mixin.get_work_pattern("NonExistent") is None
    def test_list_work_patterns(self):
"""
Test listing work patterns.        mixin = OrchestratorWorkPatternMixin()

        pattern1 = MagicMock()
        pattern1.name = "Pattern1""        pattern2 = MagicMock()
        pattern2.name = "Pattern2"
        mixin.register_work_pattern(pattern1)
        mixin.register_work_pattern(pattern2)

        patterns = mixin.list_work_patterns()
        assert set(patterns) == {"Pattern1", "Pattern2"}
    @pytest.mark.asyncio
    async def test_execute_with_pattern(self):
"""
Test executing with a work pattern.        mixin = OrchestratorWorkPatternMixin()

        # Create mock pattern
        pattern = MagicMock()
        pattern.name = "TestPattern""        pattern.execute = AsyncMock(return_value={"result": "success"})"        mixin.register_work_pattern(pattern)

        context = CascadeContext(task_id="test_task")
        result = await mixin.execute_with_pattern(context, "TestPattern")
        assert result == {"result": "success"}"        pattern.execute.assert_called_once_with(context)

    @pytest.mark.asyncio
    async def test_execute_with_default_pattern(self):
"""
Test executing with default pattern.        mixin = OrchestratorWorkPatternMixin()

        # Create mock pattern
        pattern = MagicMock()
        pattern.name = "TestPattern""        pattern.execute = AsyncMock(return_value={"result": "success"})"        mixin.register_work_pattern(pattern)

        context = CascadeContext(task_id="test_task")
        result = await mixin.execute_with_pattern(context)

        assert result == {"result": "success"}
    @pytest.mark.asyncio
    async def test_execute_with_pattern_not_found(self):
"""
Test executing with non-existent pattern.        mixin = OrchestratorWorkPatternMixin()

        context = CascadeContext(task_id="test_task")
        with pytest.raises(ValueError, match="Work pattern 'NonExistent' not found"):"'            await mixin.execute_with_pattern(context, "NonExistent")"
    @pytest.mark.asyncio
    async def test_execute_without_default_pattern(self):
"""
Test executing without default pattern set.        mixin = OrchestratorWorkPatternMixin()

        context = CascadeContext(task_id="test_task")
        with pytest.raises(ValueError, match="No work pattern specified and no default pattern set"):"            await mixin.execute_with_pattern(context)

    def test_validate_work_pattern_setup_valid(self):
"""
Test validating a valid work pattern setup.        mixin = OrchestratorWorkPatternMixin()

        pattern = MagicMock()
        pattern.name = "TestPattern""        pattern.validate_agents.return_value = True
        mixin.register_work_pattern(pattern)

        assert mixin.validate_work_pattern_setup("TestPattern") is True
    def test_validate_work_pattern_setup_invalid_agents(self):
"""
Test validating a pattern with invalid agents.        mixin = OrchestratorWorkPatternMixin()

        pattern = MagicMock()
        pattern.name = "TestPattern""        pattern.validate_agents.return_value = False
        mixin.register_work_pattern(pattern)

        assert mixin.validate_work_pattern_setup("TestPattern") is False
    def test_validate_work_pattern_setup_not_found(self):
"""
Test validating a non-existent pattern.        mixin = OrchestratorWorkPatternMixin()

        assert mixin.validate_work_pattern_setup("NonExistent") is False