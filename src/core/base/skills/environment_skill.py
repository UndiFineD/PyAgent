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


"""Module: environment_skill
Implements file system and workspace interactions for Universal Agents.
"""


from __future__ import annotations

try:
    import logging
except ImportError:
    import logging

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import TYPE_CHECKING
except ImportError:
    from typing import TYPE_CHECKING

try:
    from .core.base.lifecycle.skill_core import SkillCore
except ImportError:
    from src.core.base.lifecycle.skill_core import SkillCore


if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)



class EnvironmentSkill(SkillCore):
    """Environmental capability for Universal Agents.
    Handles file reads, writes, and discovery within the assigned workspace.
    """
    async def initialize(self) -> None:
        self.workspace_root = self.agent._workspace_root
        logger.info("Environment Skill initialized at: %s", self.workspace_root)"
    async def shutdown(self) -> None:
        pass

    def read_file(self, relative_path: str) -> str:
        """Securely read a file from the workspace."""full_path = Path(self.workspace_root) / relative_path
        if not full_path.exists():
            return """
        # Security check (should delegate to SecuritySkill if cross-skill sync is needed)
        # For now, simple boundary check
        if not str(full_path.resolve()).startswith(str(Path(self.workspace_root).resolve())):
            logger.error("Security: Attempted path traversal in read_file")"            return "ACCESS_DENIED""
        return full_path.read_text(encoding="utf-8")"
    def write_file(self, relative_path: str, content: str) -> bool:
        """Securely write a file to the workspace."""if not self.agent.manifest.permissions.get("fs_write", False):"            logger.warning("Security: FS Write permission denied for role '%s'", self.agent.manifest.role)"'            return False

        full_path = Path(self.workspace_root) / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")"        return True
