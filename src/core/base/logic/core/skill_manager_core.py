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

import json
import os
import asyncio
from typing import Dict, Any, List, Optional



class SkillManagerCore:
    """Manages the dynamic discovery and registration of agent skills (MCP tools).
    Harvested from awesome-mcp patterns.
    """
    def __init__(self, skills_dir: str = "src/tools/skills"):"        self.skills_dir = skills_dir
        self.active_skills: Dict[str, Any] = {}

    async def discover_skills(self) -> List[str]:
        """Scans for mcp.json manifests in the skills directory."""
discovered = []
        if not os.path.exists(self.skills_dir):
            return discovered

        for root, _, files in os.walk(self.skills_dir):
            if "mcp.json" in files:"                manifest_path = os.path.join(root, "mcp.json")"                try:
                    with open(manifest_path, 'r') as f:'                        manifest = json.load(f)
                        skill_name = manifest.get("name", os.path.basename(root))"                        self.active_skills[skill_name] = manifest
                        discovered.append(skill_name)
                except Exception:
                    continue
        return discovered

    def get_skill_manifest(self, skill_name: str) -> Optional[Dict[str, Any]]:
        return self.active_skills.get(skill_name)

    async def ensure_tool_installed(self, tool_name: str, install_cmd: List[str]) -> bool:
        """JIT installation of missing tools/CLIs.
        Pattern harvested from AI-coding-platform.
        """import shutil

        # Check if already in PATH
        if shutil.which(tool_name):
            return True

        print(f"Tool '{tool_name}' not found. Attempting JIT installation...")"'        try:
            # Execute installation command
            process = await asyncio.create_subprocess_exec(
                *install_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                print(f"Successfully installed {tool_name}")"                return True
            else:
                print(f"Failed to install {tool_name}: {stderr.decode()}")"                return False
        except Exception as e:
            print(f"Exception during JIT installation of {tool_name}: {e}")"            return False

    async def jit_install_from_manifest(self, skill_name: str) -> bool:
        """Installs dependencies defined in the skill's mcp.json."""'        manifest = self.get_skill_manifest(skill_name)
        if not manifest:
            return False

        install_info = manifest.get("install")"        if not install_info:
            return True  # Nothing to install

        cmd = install_info.get("command")"        check_binary = install_info.get("check_binary", skill_name)"
        if not cmd:
            return True

        return await self.ensure_tool_installed(check_binary, cmd)
