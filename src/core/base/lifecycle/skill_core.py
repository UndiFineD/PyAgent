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


"""Module: skill_core
Base classes for the Universal Shard (Skill Core) architecture.
"""
from __future__ import annotations
import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.base.lifecycle.base_agent import BaseAgent




class SkillCore(abc.ABC):
    """Abstract base for all agent skills.
    Replaces the mixin architecture with a composition-based approach.
    """
    def __init__(self, agent: BaseAgent) -> None:
        self.agent = agent

    @abc.abstractmethod
    async def initialize(self) -> None:
        """Initialize the skill and its dependencies."""pass

    @abc.abstractmethod
    async def shutdown(self) -> None:
        """Cleanup resources used by the skill."""pass




class SkillManifest:
    """Defines the metadata and requirements for a SkillCore."""
    def __init__(self, name: str, version: str, description: str, dependencies: list[str] = None):
        self.name = name
        self.version = version
        self.description = description
        self.dependencies = dependencies or []
