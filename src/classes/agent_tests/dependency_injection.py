#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");

"""Dependency injection for tests."""

from typing import Any, Dict, Optional

from .models import TestDependency


class DependencyInjector:
    """Test dependency injection framework."""

    def __init__(self) -> None:
        """Initialize dependency injector."""
        self.dependencies: Dict[str, TestDependency] = {}
        self.overrides: Dict[str, Any] = {}
        self._scopes: Dict[str, str] = {}

    def register(
        self,
        name: str,
        dependency_type: str,
        implementation: str = "",
        mock_behavior: str = "",
        scope: str = "function"
    ) -> TestDependency:
        """Register a dependency."""
        dep = TestDependency(
            name=name,
            dependency_type=dependency_type,
            implementation=implementation,
            mock_behavior=mock_behavior
        )
        self.dependencies[name] = dep
        self._scopes[name] = scope
        return dep

    def override(self, name: str, value: Any) -> None:
        """Override a dependency with a specific value."""
        self.overrides[name] = value

    def clear_override(self, name: str) -> bool:
        """Clear a dependency override."""
        if name in self.overrides:
            del self.overrides[name]
            return True
        return False

    def resolve(self, name: str) -> Optional[Any]:
        """Resolve a dependency."""
        if name in self.overrides:
            return self.overrides[name]
        dep = self.dependencies.get(name)
        if not dep:
            return None
        return dep.implementation

    def get_fixture_code(self, name: str) -> str:
        """Generate pytest fixture code for a dependency."""
        dep = self.dependencies.get(name)
        if not dep:
            return ""
        scope = self._scopes.get(name, "function")
        return (
            f"@pytest.fixture(scope='{scope}')\n"
            f"def {name}() -> {dep.dependency_type}:\n"
            f"    \"\"\"{name} fixture.\"\"\"\n"
            f"    {dep.implementation or 'pass'}\n"
        )

    def get_all_fixtures(self) -> str:
        """Generate all fixture code."""
        fixtures: list[str] = []
        for name in self.dependencies:
            fixtures.append(self.get_fixture_code(name))
        return "\n".join(fixtures)
