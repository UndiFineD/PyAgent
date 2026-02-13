#!/usr/bin/env python3
# Refactored by copilot-placeholder
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


"""Environment and data management for tests."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .models import TestEnvironment

__version__ = VERSION


def _empty_str_list() -> list[str]:
    return []


def _empty_dict_any() -> dict[str, Any]:
    return {}


class EnvironmentProvisioner:
    """Provision test environments."""

    @dataclass
    class ProvisionedEnvironment:
        """Represents a provisioned development or testing environment."""

        status: str
        python_version: str = ""
        dependencies: list[str] = field(default_factory=_empty_str_list)
        config: dict[str, Any] = field(default_factory=_empty_dict_any)

    def __init__(self) -> None:
        """Initialize environment provisioner."""
        self.environments: dict[str, TestEnvironment] = {}
        self.active: dict[str, bool] = {}
        self._setup_logs: dict[str, list[str]] = {}
        self._provisioned: list[EnvironmentProvisioner.ProvisionedEnvironment] = []

    def register_environment(
        self,
        name: str,
        base_url: str = "",
        variables: dict[str, str] | None = None,
        fixtures: list[str] | None = None,
        setup_commands: list[str] | None = None,
        teardown_commands: list[str] | None = None,
    ) -> TestEnvironment:
        """Register a test environment."""
        env = TestEnvironment(
            name=name,
            base_url=base_url,
            variables=variables or {},
            fixtures=fixtures or [],
            setup_commands=setup_commands or [],
            teardown_commands=teardown_commands or [],
        )
        self.environments[name] = env
        self.active[name] = False
        self._setup_logs[name] = []
        return env

    def provision(self, name: dict[str, Any] | str) -> dict[str, Any]:
        """Provision an environment."""
        if isinstance(name, dict):
            env = EnvironmentProvisioner.ProvisionedEnvironment(
                status="ready",
                python_version=str(name.get("python_version", "")),
                dependencies=list(name.get("dependencies", []) or []),
                config=dict(name),
            )
            self._provisioned.append(env)
            return env

        name_key = name
        env = self.environments.get(name_key)
        if not env:
            return {"error": "Environment not found", "success": False}

        if self.active.get(name_key):
            return {"warning": "Already active", "success": True}

        for cmd in env.setup_commands:
            self._setup_logs.setdefault(name_key, []).append(f"Executed: {cmd}")
        self.active[name_key] = True
        return {"environment": name_key, "success": True, "variables": env.variables}

    def cleanup(self, env: Any) -> None:
        """Cleanup a provisioned environment (compat API)."""
        if hasattr(env, "status"):
            try:
                env.status = "cleaned"
            except (AttributeError, ValueError):
                pass

    def teardown(self, name: str) -> dict[str, Any]:
        """Teardown an environment."""
        env = self.environments.get(name)

        if not env:
            return {"error": "Environment not found", "success": False}
        for cmd in env.teardown_commands:
            self._setup_logs[name].append(f"Teardown: {cmd}")
        self.active[name] = False
        return {"environment": name, "success": True}

    def get_active_environments(self) -> list[str]:
        """Get list of active environments."""
        return [name for name, active in self.active.items() if active]

    def get_logs(self, name: str) -> list[str]:
        """Get setup / teardown logs for an environment."""
        return self._setup_logs.get(name, [])


class DataFactory:
    """Factory for creating test data."""

    def __init__(self, seed: int = 0) -> None:
        """Initialize data factory."""
        self.defaults: dict[str, Any] = {}
        self._schemas: dict[str, dict[str, Any]] = {}
        self._rng = random.Random(seed)
        self._auto_inc: dict[str, int] = {}

    def set_default(self, key: str, value: Any) -> None:
        """Set default value (legacy)."""
        self.defaults[key] = value

    def register(self, kind: str, schema: dict[str, Any]) -> None:
        """Register a schema for a named kind."""
        self._schemas[kind] = dict(schema)

    def _generate_value(self, kind: str, spec: Any) -> Any:
        if spec == "auto_increment":
            self._auto_inc[kind] = self._auto_inc.get(kind, 0) + 1
            return self._auto_inc[kind]
        if spec == "random_string":
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            return "".join(self._rng.choice(alphabet) for _ in range(8))
        if spec == "random_email":
            local = self._generate_value(kind, "random_string")
            domain = "example.com"
            return f"{local}@{domain}"
        if spec == "random_int":
            return self._rng.randint(0, 1000)
        return spec

    def create(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Create data."""
        if args and isinstance(args[0], str):
            kind: str = args[0]
            overrides: dict[str, Any] = kwargs.get("overrides") or {}
            schema = self._schemas.get(kind, {})
            obj: dict[str, Any] = {}
            for field_name, spec in schema.items():
                obj[field_name] = self._generate_value(kind, spec)
            obj.update(overrides)
            return obj

        result = dict(self.defaults)
        result.update(kwargs)
        return result

    def create_batch(self, kind: str, count: int, overrides: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Create a batch of objects for a kind."""
        return [self.create(kind, overrides=overrides or {}) for _ in range(count)]
