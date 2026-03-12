#!/usr/bin/env python3
"""Skills registry module for PyAgent."""
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

from __future__ import annotations

from pathlib import Path

import yaml


class SkillsRegistry:
    """A registry for managing available skills in the PyAgent ecosystem."""

    def __init__(self, skills_dir: Path):
        """Initialize the SkillsRegistry with a directory containing skill YAML files."""
        self.skills_dir = Path(skills_dir)

    async def list_skills(self) -> list[str]:
        """List the names of all skills available in the registry."""
        names: list[str] = []
        for path in self.skills_dir.glob("*.yaml"):
            try:
                data = yaml.safe_load(path.read_text())
                if isinstance(data, dict) and "name" in data:
                    names.append(data["name"])
            except Exception:
                continue
        return names
