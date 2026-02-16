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
Core protocols and interfaces for the PyAgent framework.
Provides structural typing (Protocols) for agents, orchestrators, and components.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@runtime_checkable
class AgentInterface(Protocol):
    """
    Core interface for all AI-powered agents.
    Defining this as a Protocol facilitates future Rust implementation (PyO3).
    """

    file_path: Path

    previous_content: str

    current_content: str

    def read_previous_content(self) -> str:
        """Reads the original content of the file."""
        raise NotImplementedError()

    def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Applies AI reasoning to improve file content."""
        raise NotImplementedError()

    def update_file(self) -> bool:
        """Commits changes to the file system via StateTransaction."""
        raise NotImplementedError()

    def get_diff(self) -> str:
        """Returns a unified diff of changes."""
        raise NotImplementedError()

    # Advanced features that might be offloaded to Rust later

    def calculate_metrics(self, content: str | None = None) -> Any:
        """Calculates complexity and quality metrics."""
        raise NotImplementedError()

    def scan_for_secrets(self, content: str) -> list[str]:
        """Scans content for sensitive keys or passwords."""
        raise NotImplementedError()


@runtime_checkable
class OrchestratorInterface(Protocol):
    """Interface for fleet orchestrators."""

    def execute_task(self, task: str) -> str:
        """Executes a high-level swarm task."""
        raise NotImplementedError()

    def get_status(self) -> dict[str, Any]:
        """Returns current status of the orchestrator."""
        raise NotImplementedError()


@runtime_checkable
class CoreInterface(Protocol):
    """Pure logic interface. High-performance, no-IO, candidate for Rust parity."""

    def process_data(self, data: Any) -> Any:
        """Processes raw data into structured output."""
        raise NotImplementedError()

    def validate(self, content: str) -> bool:
        """Validates content against internal rules."""
        raise NotImplementedError()

    def get_metadata(self) -> dict[str, Any]:
        """Returns metadata about the core logic state."""
        raise NotImplementedError()


@runtime_checkable
class ContextRecorderInterface(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for cognitive recording and context harvesting."""

    def record_interaction(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        provider: str,
        model: str,
        prompt: str,
        result: str,
        meta: dict[str, Any] | None = None,
    ) -> None:
        """Records an LLM interaction for audit and lineage."""
        raise NotImplementedError()


@runtime_checkable
class Loadable(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for objects that can load their state from disk."""

    def load(self, path: Path | None = None) -> bool:
        """Loads state from file."""


@runtime_checkable
class Saveable(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for objects that can save their state to disk."""

    def save(self, path: Path | None = None) -> bool:
        """Saves state to file."""


@runtime_checkable
class Component(Protocol):  # pylint: disable=too-few-public-methods
    """Base interface for all PyAgent components with a name and version."""

    name: str
    version: str
