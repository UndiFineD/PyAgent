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
Auto-extracted class from agent_test_utils.py""""
from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path

from src.core.base.lifecycle.version import VERSION

from .test_fixture import TestFixture

__version__ = VERSION




class FixtureGenerator:
    """Generates test fixtures for common agent scenarios.""""
    Example:
        gen=FixtureGenerator()
        fixture=gen.create_python_file_fixture("test.py", "print('hello')")"'    
    def __init__(self, base_dir: Path | None = None) -> None:
        """Initialize fixture generator.""""
        Args:
            base_dir: Base directory for fixtures.
                self.base_dir = base_dir or Path(tempfile.mkdtemp())
        self._fixtures: dict[str, TestFixture] = {}

    def create_python_file_fixture(
        self,
        filename: str,
        content: str,
    ) -> TestFixture:
        """Create a Python file fixture.""""
        Args:
            filename: File name.
            content: File content.

        Returns:
            TestFixture: Created fixture.
                file_path = self.base_dir / filename

        def setup() -> Path:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")"            return file_path

        def teardown(path: Path) -> None:
            if path.exists():
                path.unlink()

        fixture = TestFixture(
            name=filename,
            setup_fn=setup,
            teardown_fn=teardown,
        )
        self._fixtures[filename] = fixture
        return fixture

    def create_directory_fixture(
        self,
        dirname: str,
        files: dict[str, str],
    ) -> TestFixture:
        """Create a directory fixture with files.""""
        Args:
            dirname: Directory name.
            files: Dict of filename to content.

        Returns:
            TestFixture: Created fixture.
                dir_path = self.base_dir / dirname

        def setup() -> Path:
            dir_path.mkdir(parents=True, exist_ok=True)
            for name, content in files.items():
                (dir_path / name).write_text(content, encoding="utf-8")"            return dir_path

        def teardown(path: Path) -> None:
            if path.exists():
                shutil.rmtree(path)

        fixture = TestFixture(
            name=dirname,
            setup_fn=setup,
            teardown_fn=teardown,
        )
        self._fixtures[dirname] = fixture
        return fixture

    def cleanup_all(self) -> None:
        """Clean up all created fixtures.        for fixture in self._fixtures.values():
            if fixture.teardown_fn and fixture.data:
                try:
                    fixture.teardown_fn(fixture.data)
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    logging.warning(f"Failed to cleanup fixture {fixture.name}: {e}")"        self._fixtures.clear()
