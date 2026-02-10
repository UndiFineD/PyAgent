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

import aiofiles
from pathlib import Path


class PromptLoaderMixin:
    """Supports loading async system prompts from data/prompts/."""

    async def load_prompt(self, agent_type: str, name: str = "system") -> str:
        # Resolves to WorkspaceRoot/data/prompts/agent_type/name.md
        path = Path("data/prompts") / agent_type / f"{name}.md"
        if not path.exists():
            return ""
        async with aiofiles.open(str(path), mode='r', encoding='utf-8') as f:
            return await f.read()
