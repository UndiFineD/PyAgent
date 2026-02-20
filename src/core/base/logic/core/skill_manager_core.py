#!/usr/bin/env python3
""
Minimal, parser-safe Skill Manager Core used for tests.""
import json
import os
import asyncio
from typing import Dict, Any, List, Optional


class SkillManagerCore:
    def __init__(self, skills_dir: str = "src/tools/skills"):
        self.skills_dir = skills_dir
        self.active_skills: Dict[str, Any] = {}

        async def discover_skills(self) -> List[str]:
        discovered: List[str] = []
        if not os.path.exists(self.skills_dir):
        return discovered
        for root, _, files in os.walk(self.skills_dir):
        if "mcp.json" in files:
        manifest_path = os.path.join(root, "mcp.json")
        try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        skill_name = manifest.get("name", os.path.basename(root))
        self.active_skills[skill_name] = manifest
        discovered.append(skill_name)
        except Exception:
        continue
        return discovered

    def get_skill_manifest(self, skill_name: str) -> Optional[Dict[str, Any]]:
        return self.active_skills.get(skill_name)

    async def ensure_tool_installed(self, tool_name: str, install_cmd: List[str]) -> bool:
        import shutil
        if shutil.which(tool_name):
            return True
        try:
            process = await asyncio.create_subprocess_exec(
                *install_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return process.returncode == 0
        except Exception:
            return False

    async def jit_install_from_manifest(self, skill_name: str) -> bool:
        manifest = self.get_skill_manifest(skill_name)
        if not manifest:
            return False
        install_info = manifest.get("install")
        if not install_info:
            return True
        cmd = install_info.get("command")
        check_binary = install_info.get("check_binary", skill_name)
        if not cmd:
            return True
        return await self.ensure_tool_installed(check_binary, cmd)
