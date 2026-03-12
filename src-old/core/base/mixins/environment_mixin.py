#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/mixins/environment_mixin.description.md

# environment_mixin

**File**: `src\core\base\mixins\environment_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 164  
**Complexity**: 1 (simple)

## Overview

Module: environment_mixin
Provides environment management capabilities to agents.

## Classes (1)

### `EnvironmentMixin`

Mixin providing environment management capabilities to agents.
Allows agents to create and manage isolated execution environments.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `contextlib.asynccontextmanager`
- `logging`
- `os`
- `src.core.base.common.models.base_models.EnvironmentConfig`
- `src.core.base.common.models.base_models.EnvironmentInstance`
- `src.core.base.common.models.core_enums.EnvironmentIsolation`
- `src.core.base.environment.get_environment_manager`
- `src.core.base.lifecycle.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/environment_mixin.improvements.md

# Improvements for environment_mixin

**File**: `src\core\base\mixins\environment_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 164 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `environment_mixin_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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
Module: environment_mixin
Provides environment management capabilities to agents.
"""


import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from src.core.base.common.models.base_models import (
    EnvironmentConfig,
    EnvironmentInstance,
)
from src.core.base.common.models.core_enums import EnvironmentIsolation
from src.core.base.environment import get_environment_manager
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

logger = logging.getLogger(__name__)


class EnvironmentMixin:
    """
    Mixin providing environment management capabilities to agents.
    Allows agents to create and manage isolated execution environments.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._env_manager = None
        self._active_environments: Dict[str, EnvironmentInstance] = {}

    async def _get_env_manager(self):
        """Get the environment manager instance."""
        if self._env_manager is None:
            self._env_manager = await get_environment_manager()
        return self._env_manager

    async def create_environment_config(
        self,
        name: str,
        version: str = "1.0.0",
        description: str = "",
        isolation: EnvironmentIsolation = EnvironmentIsolation.NONE,
        cpu_limit: float = 1.0,
        memory_limit: int = 1024,
        disk_limit: int = 10240,
        ttl_seconds: int = 1800,
        **kwargs,
    ) -> EnvironmentConfig:
        """Create a new environment configuration."""
        config = EnvironmentConfig(
            name=name,
            version=version,
            description=description,
            isolation=isolation,
            cpu_limit=cpu_limit,
            memory_limit=memory_limit,
            disk_limit=disk_limit,
            ttl_seconds=ttl_seconds,
            **kwargs,
        )

        manager = await self._get_env_manager()
        await manager.register_environment(config)

        logger.info(f"Created environment config: {name}@{version}")
        return config

    @asynccontextmanager
    async def use_environment(
        self,
        env_name: str,
        env_version: str = "1.0.0",
        custom_config: Optional[Dict[str, Any]] = None,
    ):
        """Context manager for using an environment instance."""
        manager = await self._get_env_manager()

        async with manager.create_instance(
            env_name, env_version, custom_config
        ) as instance:
            self._active_environments[instance.id] = instance
            try:
                yield instance
            finally:
                self._active_environments.pop(instance.id, None)

    async def list_available_environments(self) -> list[EnvironmentConfig]:
        """List all available environment configurations."""
        manager = await self._get_env_manager()
        return await manager.list_environments()

    async def get_environment_status(
        self, instance_id: str
    ) -> Optional[EnvironmentInstance]:
        """Get the status of an environment instance."""
        manager = await self._get_env_manager()
        return await manager.get_instance(instance_id)

    async def cleanup_environments(self) -> None:
        """Clean up all active environments for this agent."""
        for instance_id in list(self._active_environments.keys()):
            try:
                manager = await self._get_env_manager()
                await manager._terminate_instance(instance_id)
            except Exception as e:
                logger.error(f"Error cleaning up environment {instance_id}: {e}")

        self._active_environments.clear()

    async def switch_environment_context(
        self, instance_id: str, operation: callable
    ) -> Any:
        """Switch to a specific environment context for an operation."""
        instance = self._active_environments.get(instance_id)
        if not instance:
            raise ValueError(f"Environment instance {instance_id} not active")

        # TODO: Implement context switching logic
        # This could involve changing working directory, environment variables, etc.

        try:
            # Set environment variables for this instance
            old_env = {}
            for key, value in instance.environment_variables.items():
                env_key = f"{instance.id}_{key}"
                old_env[key] = os.environ.get(key)
                os.environ[key] = value

            # Change to working directory if specified
            old_cwd = None
            if instance.working_directory:
                old_cwd = os.getcwd()
                os.chdir(instance.working_directory)

            # Execute operation
            result = await operation()

            return result

        finally:
            # Restore environment
            for key, old_value in old_env.items():
                if old_value is not None:
                    os.environ[key] = old_value
                else:
                    os.environ.pop(key, None)

            if old_cwd:
                os.chdir(old_cwd)
