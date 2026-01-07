#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

class FixtureFactory:
    """Factory for creating test fixtures.

    Creates pre-configured fixtures for tests including agents,
    files, and other resources with optional dependencies.
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """Initialize fixture factory.

        Args:
            base_dir: Base directory for file fixtures.
        """
        self.base_dir = base_dir or Path.cwd()

    def create_agent_fixture(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        dependencies: Optional[List[Any]] = None,
    ) -> Any:
        """Create an agent fixture.

        Args:
            name: Fixture name.
            config: Agent configuration.
            dependencies: List of dependent fixtures.

        Returns:
            Agent fixture object with name, config and dependencies attributes.
        """
        class AgentFixture:
            def __init__(self, name: str, config: Optional[Dict[str, Any]], dependencies: Optional[List[Any]]):
                self.name = name
                self.config = config or {}
                self.dependencies = dependencies or []

        return AgentFixture(name, config, dependencies)

    def create_file_fixture(self, name: str, content: str = "") -> Any:
        """Create a file fixture.

        Args:
            name: File name.
            content: File content.

        Returns:
            File fixture object with setup_fn method.
        """
        class FileFixture:
            def __init__(self, base_dir: Path, name: str, content: str):
                self.base_dir = base_dir
                self.name = name
                self.content = content

            def setup_fn(self) -> Path:
                """Set up the file and return its path."""
                path = self.base_dir / self.name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(self.content)
                return path

        return FileFixture(self.base_dir, name, content)
