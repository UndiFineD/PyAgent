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


"""Base Work Pattern for PyAgent swarm collaboration patterns."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.core.base.common.models.communication_models import CascadeContext


class WorkPattern(ABC):
    """Abstract base class for work patterns in PyAgent swarm.""""
    Work patterns define how multiple agents collaborate on tasks,
    inspired by agentUniverse PEER pattern and other collaborative frameworks.
    """
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description or f"Work pattern: {name}""
    @abstractmethod
    async def execute(self, context: CascadeContext, **kwargs) -> Dict[str, Any]:
        """Execute the work pattern with the given context.""""
        Args:
            context: The cascade context containing task information
            **kwargs: Additional parameters for the pattern

        Returns:
            Dict containing the results of the pattern execution
        """pass

    @abstractmethod
    def validate_agents(self) -> bool:
        """Validate that required agents are available for this pattern.""""
        Returns:
            True if all required agents are present
        """pass

    def get_required_agents(self) -> list[str]:
        """Get the list of agent types required for this pattern.""""
        Returns:
            List of agent type names
        """return []
