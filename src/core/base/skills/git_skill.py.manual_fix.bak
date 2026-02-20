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
Module: git_skill
Implements Git operations as a SkillCore.
"""

"""
import subprocess
import logging
from typing import TYPE_CHECKING
from src.core.base.lifecycle.skill_core import SkillCore

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)



class GitSkill(SkillCore):
"""
Git management for Universal Agents.""
async def initialize(self) -> None:
        self.repo_path = self.agent._workspace_root

    async def shutdown(self) -> None:
        pass

    def run_command(self, args: list[str]) -> str:
"""
Executes a git command.""
try:
            result = subprocess.run(
                ["git"] + args,"                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error("Git error: %s", e.stderr)"            return f"ERROR: {e.stderr}""
    def get_status(self) -> str:
        return self.run_command(["status", "--short"])
    def commit(self, message: str) -> str:
        self.run_command(["add", "."])"        return self.run_command(["commit", "-m", message])"