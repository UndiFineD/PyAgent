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
Module: environment_manager
Provides environment management for PyAgent multi-agent architecture.
Inspired by AEnvironment patterns for isolation and resource management.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import tempfile
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.base.common.models.base_models import EnvironmentConfig, EnvironmentInstance
from src.core.base.common.models.core_enums import EnvironmentStatus, EnvironmentIsolation
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

logger = logging.getLogger(__name__)


class EnvironmentManager:
    """
    Manages agent environments with isolation, resource limits, and lifecycle management.
    Inspired by AEnvironment's containerized environment approach.
    """

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path("data/environments")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.environments: Dict[str, EnvironmentConfig] = {}
        self.instances: Dict[str, EnvironmentInstance] = {}
        self._cleanup_task: Optional[asyncio.Task] = None

    async def initialize(self) -> None:
        """Initialize the environment manager."""
        await self._load_environments()
        await self._load_instances()
        self._start_cleanup_task()

    async def shutdown(self) -> None:
        """Shutdown the environment manager."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        await self._cleanup_expired_instances()

    def _start_cleanup_task(self) -> None:
        """Start the background cleanup task."""
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _cleanup_loop(self) -> None:
        """Background task to cleanup expired environments."""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                await self._cleanup_expired_instances()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")

    async def _cleanup_expired_instances(self) -> None:
        """Cleanup expired environment instances."""
        expired_instances = [
            instance_id for instance_id, instance in self.instances.items()
            if instance.is_expired() and instance.status != EnvironmentStatus.TERMINATED
        ]

        for instance_id in expired_instances:
            logger.info(f"Cleaning up expired environment instance: {instance_id}")
            await self._terminate_instance(instance_id)

    async def register_environment(self, config: EnvironmentConfig) -> None:
        """Register a new environment configuration."""
        env_key = f"{config.name}@{config.version}"
        self.environments[env_key] = config
        await self._save_environments()

    async def unregister_environment(self, name: str, version: str) -> None:
        """Unregister an environment configuration."""
        env_key = f"{name}@{version}"
        if env_key in self.environments:
            del self.environments[env_key]
            await self._save_environments()

    async def get_environment(self, name: str, version: str) -> Optional[EnvironmentConfig]:
        """Get environment configuration."""
        env_key = f"{name}@{version}"
        return self.environments.get(env_key)

    async def list_environments(self) -> List[EnvironmentConfig]:
        """List all registered environments."""
        return list(self.environments.values())

    @asynccontextmanager
    async def create_instance(
        self,
        env_name: str,
        env_version: str = "1.0.0",
        custom_config: Optional[Dict[str, Any]] = None
    ):
        """Create and manage an environment instance with context manager."""
        instance = await self._create_instance(env_name, env_version, custom_config)
        try:
            yield instance
        finally:
            await self._terminate_instance(instance.id)

    async def _create_instance(
        self,
        env_name: str,
        env_version: str,
        custom_config: Optional[Dict[str, Any]] = None
    ) -> EnvironmentInstance:
        """Create a new environment instance."""
        config = await self.get_environment(env_name, env_version)
        if not config:
            raise ValueError(f"Environment {env_name}@{env_version} not found")

        instance_id = str(uuid.uuid4())
        expires_at = time.time() + config.ttl_seconds

        # Merge environment variables
        env_vars = config.environment_variables.copy()
        if custom_config and "environment_variables" in custom_config:
            env_vars.update(custom_config["environment_variables"])

        instance = EnvironmentInstance(
            id=instance_id,
            environment_name=f"{env_name}@{env_version}",
            expires_at=expires_at,
            environment_variables=env_vars,
            metadata=custom_config or {}
        )

        self.instances[instance_id] = instance
        await self._save_instances()

        # Initialize the instance based on isolation level
        await self._initialize_instance(instance, config)

        return instance

    async def _initialize_instance(
        self,
        instance: EnvironmentInstance,
        config: EnvironmentConfig
    ) -> None:
        """Initialize the environment instance based on isolation level."""
        try:
            instance.update_status(EnvironmentStatus.CREATING)

            if config.isolation == EnvironmentIsolation.NONE:
                # No isolation - just set up working directory
                instance.working_directory = Path(tempfile.mkdtemp(prefix=f"env_{instance.id}_"))
                instance.working_directory.mkdir(parents=True, exist_ok=True)

            elif config.isolation == EnvironmentIsolation.PROCESS:
                # Process isolation - could spawn subprocess
                instance.working_directory = Path(tempfile.mkdtemp(prefix=f"env_{instance.id}_"))
                instance.working_directory.mkdir(parents=True, exist_ok=True)
                # TODO: Implement process spawning

            elif config.isolation == EnvironmentIsolation.CONTAINER:
                # Container isolation - Docker/Kubernetes
                # TODO: Implement container creation
                pass

            # Set up environment variables
            for key, value in instance.environment_variables.items():
                os.environ[f"{instance.id}_{key}"] = value

            instance.update_status(EnvironmentStatus.RUNNING)
            await self._save_instances()

        except Exception as e:
            logger.error(f"Failed to initialize instance {instance.id}: {e}")
            instance.update_status(EnvironmentStatus.FAILED)
            await self._save_instances()
            raise

    async def _terminate_instance(self, instance_id: str) -> None:
        """Terminate an environment instance."""
        instance = self.instances.get(instance_id)
        if not instance:
            return

        try:
            instance.update_status(EnvironmentStatus.TERMINATED)

            # Clean up working directory
            if instance.working_directory and instance.working_directory.exists():
                import shutil
                shutil.rmtree(instance.working_directory)

            # Clean up environment variables
            for key in instance.environment_variables.keys():
                env_key = f"{instance.id}_{key}"
                os.environ.pop(env_key, None)

            # Clean up container/process if needed
            if instance.container_id:
                # TODO: Stop container
                pass
            if instance.process_id:
                # TODO: Kill process
                pass

        except Exception as e:
            logger.error(f"Error terminating instance {instance_id}: {e}")
        finally:
            # Remove from instances
            self.instances.pop(instance_id, None)
            await self._save_instances()

    async def get_instance(self, instance_id: str) -> Optional[EnvironmentInstance]:
        """Get environment instance by ID."""
        return self.instances.get(instance_id)

    async def list_instances(self) -> List[EnvironmentInstance]:
        """List all active environment instances."""
        return list(self.instances.values())

    async def _load_environments(self) -> None:
        """Load environment configurations from disk."""
        env_file = self.base_dir / "environments.json"
        if env_file.exists():
            try:
                data = json.loads(env_file.read_text())
                for env_data in data:
                    # Convert string back to enum
                    if 'isolation' in env_data:
                        env_data['isolation'] = EnvironmentIsolation(env_data['isolation'])
                    config = EnvironmentConfig(**env_data)
                    env_key = f"{config.name}@{config.version}"
                    self.environments[env_key] = config
            except Exception as e:
                logger.error(f"Failed to load environments: {e}")

    async def _save_environments(self) -> None:
        """Save environment configurations to disk."""
        env_file = self.base_dir / "environments.json"
        try:
            from dataclasses import asdict
            data = []
            for config in self.environments.values():
                config_dict = asdict(config)
                # Convert enum to string
                if 'isolation' in config_dict:
                    config_dict['isolation'] = config_dict['isolation'].value
                data.append(config_dict)
            env_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logger.error(f"Failed to save environments: {e}")

    async def _load_instances(self) -> None:
        """Load environment instances from disk."""
        instances_file = self.base_dir / "instances.json"
        if instances_file.exists():
            try:
                data = json.loads(instances_file.read_text())
                for instance_data in data:
                    # Convert string back to enum
                    if 'status' in instance_data:
                        instance_data['status'] = EnvironmentStatus(instance_data['status'])
                    instance = EnvironmentInstance(**instance_data)
                    self.instances[instance.id] = instance
            except Exception as e:
                logger.error(f"Failed to load instances: {e}")

    async def _save_instances(self) -> None:
        """Save environment instances to disk."""
        instances_file = self.base_dir / "instances.json"
        try:
            from dataclasses import asdict
            data = []
            for instance in self.instances.values():
                instance_dict = asdict(instance)
                # Convert enum to string
                if 'status' in instance_dict:
                    instance_dict['status'] = instance_dict['status'].value
                data.append(instance_dict)
            instances_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logger.error(f"Failed to save instances: {e}")


# Global environment manager instance
_env_manager: Optional[EnvironmentManager] = None


async def get_environment_manager() -> EnvironmentManager:
    """Get the global environment manager instance."""
    global _env_manager
    if _env_manager is None:
        _env_manager = EnvironmentManager()
        await _env_manager.initialize()
    return _env_manager
