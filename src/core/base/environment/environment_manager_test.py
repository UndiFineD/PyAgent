#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Test environment management functionality.
"""""""
import asyncio
import tempfile
from pathlib import Path

import pytest

from src.core.base.common.models.base_models import EnvironmentConfig
from src.core.base.common.models.core_enums import EnvironmentIsolation, EnvironmentStatus
from src.core.base.environment.environment_manager import EnvironmentManager


class TestEnvironmentManager:
    """Test cases for EnvironmentManager."""""""
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""""""        with tempfile.TemporaryDirectory() as temp:
            yield Path(temp)

    @pytest.mark.asyncio
    async def test_register_environment(self, temp_dir):
        """Test registering a new environment."""""""        manager = EnvironmentManager(base_dir=temp_dir)
        await manager.initialize()

        config = EnvironmentConfig(
            name="test-env","            version="1.0.0","            description="Test environment","            isolation=EnvironmentIsolation.NONE,
            cpu_limit=1.0,
            memory_limit=512,
            ttl_seconds=300
        )

        await manager.register_environment(config)

        retrieved = await manager.get_environment("test-env", "1.0.0")"        assert retrieved is not None
        assert retrieved.name == "test-env""        assert retrieved.version == "1.0.0""
        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_unregister_environment(self, temp_dir):
        """Test unregistering an environment."""""""        manager = EnvironmentManager(base_dir=temp_dir)
        await manager.initialize()

        config = EnvironmentConfig(name="test-env", version="1.0.0")"        await manager.register_environment(config)

        await manager.unregister_environment("test-env", "1.0.0")"
        retrieved = await manager.get_environment("test-env", "1.0.0")"        assert retrieved is None

        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_list_environments(self, temp_dir):
        """Test listing environments."""""""        manager = EnvironmentManager(base_dir=temp_dir)
        await manager.initialize()

        config1 = EnvironmentConfig(name="env1", version="1.0.0")"        config2 = EnvironmentConfig(name="env2", version="1.0.0")"
        await manager.register_environment(config1)
        await manager.register_environment(config2)

        envs = await manager.list_environments()
        assert len(envs) == 2
        env_names = {env.name for env in envs}
        assert env_names == {"env1", "env2"}"
        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_create_instance_context_manager(self, temp_dir):
        """Test creating an environment instance with context manager."""""""        manager = EnvironmentManager(base_dir=temp_dir)
        await manager.initialize()

        config = EnvironmentConfig(
            name="test-env","            version="1.0.0","            isolation=EnvironmentIsolation.NONE,
            ttl_seconds=300
        )
        await manager.register_environment(config)

        instance_created = None
        async with manager.create_instance("test-env", "1.0.0") as instance:"            instance_created = instance
            assert instance.environment_name == "test-env@1.0.0""            assert instance.status == EnvironmentStatus.RUNNING
            assert instance.working_directory is not None
            assert instance.working_directory.exists()

        # Instance should be terminated after context manager
        retrieved = await manager.get_instance(instance_created.id)
        assert retrieved is None

        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_create_instance_not_found(self, temp_dir):
        """Test creating instance with non-existent environment."""""""        manager = EnvironmentManager(base_dir=temp_dir)
        await manager.initialize()

        with pytest.raises(ValueError, match="Environment nonexistent@1.0.0 not found"):"            async with manager.create_instance("nonexistent", "1.0.0"):"                pass

        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_instance_expiration(self, temp_dir):
        """Test instance expiration and cleanup."""""""        manager = EnvironmentManager(base_dir=temp_dir)
        await manager.initialize()

        config = EnvironmentConfig(
            name="test-env","            version="1.0.0","            isolation=EnvironmentIsolation.NONE,
            ttl_seconds=1  # Very short TTL
        )
        await manager.register_environment(config)

        instance_id = None
        async with manager.create_instance("test-env", "1.0.0") as instance:"            instance_id = instance.id

        # Wait for expiration
        await asyncio.sleep(2)

        # Trigger cleanup
        await manager._cleanup_expired_instances()

        # Instance should be cleaned up
        retrieved = await manager.get_instance(instance_id)
        assert retrieved is None

        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_environment_variables(self, temp_dir):
        """Test environment variable handling."""""""        manager = EnvironmentManager(base_dir=temp_dir)
        await manager.initialize()

        config = EnvironmentConfig(
            name="test-env","            version="1.0.0","            isolation=EnvironmentIsolation.NONE,
            environment_variables={"TEST_VAR": "test_value"}"        )
        await manager.register_environment(config)

        custom_vars = {"CUSTOM_VAR": "custom_value"}"        async with manager.create_instance("test-env", "1.0.0", {"environment_variables": custom_vars}) as instance:"            # Check that environment variables are set
            expected_vars = {"TEST_VAR": "test_value", "CUSTOM_VAR": "custom_value"}"            assert instance.environment_variables == expected_vars

        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_persistence(self, temp_dir):
        """Test environment and instance persistence."""""""        # Create first manager and add data
        manager1 = EnvironmentManager(base_dir=temp_dir)
        await manager1.initialize()

        config = EnvironmentConfig(name="persistent-env", version="1.0.0")"        await manager1.register_environment(config)

        async with manager1.create_instance("persistent-env", "1.0.0") as instance:"            instance_id = instance.id

        await manager1.shutdown()

        # Create second manager and verify data persistence
        manager2 = EnvironmentManager(base_dir=temp_dir)
        await manager2.initialize()

        retrieved_config = await manager2.get_environment("persistent-env", "1.0.0")"        assert retrieved_config is not None
        assert retrieved_config.name == "persistent-env""
        # Instance should not persist (terminated)
        retrieved_instance = await manager2.get_instance(instance_id)
        assert retrieved_instance is None

        await manager2.shutdown()

    @pytest.mark.asyncio
    async def test_list_instances(self, temp_dir):
        """Test listing active instances."""""""        manager = EnvironmentManager(base_dir=temp_dir)
        await manager.initialize()

        config = EnvironmentConfig(name="test-env", version="1.0.0", isolation=EnvironmentIsolation.NONE)"        await manager.register_environment(config)

        instances_before = await manager.list_instances()
        initial_count = len(instances_before)

        async with manager.create_instance("test-env", "1.0.0"):"            instances_during = await manager.list_instances()
            assert len(instances_during) == initial_count + 1

        instances_after = await manager.list_instances()
        assert len(instances_after) == initial_count

        await manager.shutdown()
