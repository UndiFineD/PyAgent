#!/usr/bin/env python3
from __future__ import annotations

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
"""
Module: skill_manager
Handles dynamic loading and orchestration of SkillCore components.
"""

"""
import importlib
import logging
from typing import TYPE_CHECKING, Dict, Type

if TYPE_CHECKING:
    from src.core.base.lifecycle.base_agent import BaseAgent
    from src.core.base.lifecycle.skill_core import SkillCore

logger = logging.getLogger(__name__)



class SkillManager:
"""
Orchestrates the lifecycle of SkillCores for a Universal Agent.""
def __init__(self, agent: BaseAgent) -> None:
        self.agent = agent
        self.skills: Dict[str, SkillCore] = {}


    async def load_skill(self, skill_name: str) -> bool:
"""
Dynamically load a skill core.""
if skill_name in self.skills:
            return True

        try:
            # convention: skill 'identity' -> src.core.base.skills.identity_skill.IdentitySkill
            module_path = f"src.core.base.skills.{skill_name}_skill"
            module = importlib.import_module(module_path)

            # Find the class (should be CamelCase version of name + Skill)
            class_name = "".join(word.capitalize() for word in skill_name.split("_")) + "Skill"
            skill_class: Type[SkillCore] = getattr(module, class_name)

            skill_instance = skill_class(self.agent)
            await skill_instance.initialize()

            self.skills[skill_name] = skill_instance
            logger.info("Loaded skill: %s", skill_name)
            return True

        except (ImportError, AttributeError, Exception) as e:
            logger.error("Failed to load skill %s: %s", skill_name, e)
            return False


    async def shutdown_all(self) -> None:
"""
Shutdown all loaded skills.""
for name, skill in self.skills.items():
            try:
                await skill.shutdown()
            except Exception as e:
                logger.error("Error shutting down skill %s: %s", name, e)
        self.skills.clear()

    def get_skill(self, name: str) -> 'SkillCore | None':
"""
Retrieve a loaded skill instance.""
return self.skills.get(name)
