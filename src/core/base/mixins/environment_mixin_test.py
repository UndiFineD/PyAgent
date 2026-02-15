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
Test environment mixin functionality.
"""


import pytest

from src.core.base.common.models.core_enums import EnvironmentIsolation
from src.core.base.mixins.environment_mixin import EnvironmentMixin


class MockAgent(EnvironmentMixin):
    """Mock agent class with EnvironmentMixin."""

    def __init__(self):
        super().__init__()
        self.name = "test-agent"


class TestEnvironmentMixin:
    """Test cases for EnvironmentMixin."""

    @pytest.fixture
    def agent(self):
        """Create a mock agent with environment mixin."""
        return MockAgent()

    @pytest.mark.asyncio
    async def test_create_environment_config(self, agent):
        """Test creating environment configuration."""
        config = await agent.create_environment_config(
            name="test-env",
            version="1.0.0",
            description="Test environment",
            isolation=EnvironmentIsolation.NONE,
            cpu_limit=2.0,
            memory_limit=1024,
            ttl_seconds=600
        )

        assert config.name == "test-env"
        assert config.version == "1.0.0"
        assert config.description == "Test environment"
        assert config.isolation == EnvironmentIsolation.NONE
        assert config.cpu_limit == 2.0
        assert config.memory_limit == 1024
        assert config.ttl_seconds == 600

    @pytest.mark.asyncio
    async def test_use_environment_context_manager(self, agent):
        """Test using environment with context manager."""
        # Create config first
        await agent.create_environment_config(
            name="test-env",
            version="1.0.0",
            isolation=EnvironmentIsolation.NONE
        )

        # Use environment
        environment_used = None
        async with agent.use_environment("test-env", "1.0.0") as env_instance:
            environment_used = env_instance
            assert env_instance.environment_name == "test-env@1.0.0"
            assert env_instance.status.name == "RUNNING"

        # Environment should be cleaned up
        assert environment_used.id not in agent._active_environments

    @pytest.mark.asyncio
    async def test_list_available_environments(self, agent):
        """Test listing available environments."""
        # Get initial count
        envs = await agent.list_available_environments()
        initial_count = len(envs)

        # Add an environment with unique name
        unique_name = f"test-env-{id(agent)}"
        await agent.create_environment_config(name=unique_name, version="1.0.0")

        # Should have one more
        envs = await agent.list_available_environments()
        assert len(envs) == initial_count + 1
        assert any(env.name == unique_name for env in envs)

    @pytest.mark.asyncio
    async def test_get_environment_status(self, agent):
        """Test getting environment instance status."""
        await agent.create_environment_config(name="test-env", version="1.0.0")

        async with agent.use_environment("test-env", "1.0.0") as env_instance:
            status = await agent.get_environment_status(env_instance.id)
            assert status is not None
            assert status.id == env_instance.id
            assert status.status.name == "RUNNING"

        # After context manager, instance should be gone
        status = await agent.get_environment_status(env_instance.id)
        assert status is None

    @pytest.mark.asyncio
    async def test_cleanup_environments(self, agent):
        """Test cleaning up all environments."""
        await agent.create_environment_config(name="env1", version="1.0.0")
        await agent.create_environment_config(name="env2", version="1.0.0")

        # Create multiple instances
        instances = []
        async with agent.use_environment("env1", "1.0.0") as inst1:
            instances.append(inst1)
            async with agent.use_environment("env2", "1.0.0") as inst2:
                instances.append(inst2)
                assert len(agent._active_environments) == 2

        # All should be cleaned up after context managers
        assert len(agent._active_environments) == 0

    @pytest.mark.asyncio
    async def test_switch_environment_context(self, agent):
        """Test switching environment context."""
        await agent.create_environment_config(
            name="test-env",
            version="1.0.0",
            environment_variables={"TEST_VAR": "test_value"}
        )

        async def test_operation():
            return "operation_result"

        async with agent.use_environment("test-env", "1.0.0") as env_instance:
            # Switch context and run operation
            result = await agent.switch_environment_context(
                env_instance.id,
                test_operation
            )
            assert result == "operation_result"

    @pytest.mark.asyncio
    async def test_switch_environment_context_invalid_instance(self, agent):
        """Test switching context with invalid instance ID."""
        with pytest.raises(ValueError, match="Environment instance invalid-id not active"):
            await agent.switch_environment_context("invalid-id", lambda: None)
