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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Protocol, runtime_checkable, Any
from pathlib import Path

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

        raise NotImplementedError()



    def improve_content(self, prompt: str) -> str:
        raise NotImplementedError()


    def update_file(self) -> bool:

        raise NotImplementedError()

    def get_diff(self) -> str:
        raise NotImplementedError()

    # Advanced features that might be offloaded to Rust later


    def calculate_metrics(self, content: str | None = None) -> Any:
        raise NotImplementedError()

    def scan_for_secrets(self, content: str) -> list[str]:
        raise NotImplementedError()


@runtime_checkable
class OrchestratorInterface(Protocol):
    """Interface for fleet orchestrators."""
    def execute_task(self, task: str) -> str:
        raise NotImplementedError()



    def get_status(self) -> dict[str, Any]:
        raise NotImplementedError()




@runtime_checkable
class CoreInterface(Protocol):
    """Pure logic interface. High-performance, no-IO, candidate for Rust parity."""
    def process_data(self, data: Any) -> Any:
        raise NotImplementedError()




    def validate(self, content: str) -> bool:
        raise NotImplementedError()

    def get_metadata(self) -> dict[str, Any]:
        raise NotImplementedError()



@runtime_checkable
class ContextRecorderInterface(Protocol):
    """Interface for cognitive recording and context harvesting."""
    def record_interaction(self, provider: str, model: str, prompt: str, result: str, meta: dict[str, Any] | None = None) -> None:
        raise NotImplementedError()
