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
WorkflowState

Container for shared state and context between agents in a workflow.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class WorkflowState:
    """Maintains context, variables, and history for a multi-agent session."""

    task_id: str
    original_request: str
    variables: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)
    context_snippets: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def set(self, key: str, value: Any) -> None:
        """Sets a workflow variable."""
        self.variables[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a workflow variable."""
        return self.variables.get(key, default)

    def add_history(self, agent: str, action: str, result: str) -> None:
        """Appends an entry to the execution history."""
        self.history.append(
            {
                "agent": agent,
                "action": action,
                "result": result[:500] + "..." if len(result) > 500 else result,
            }
        )
