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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in moderation, review, and policy compliance."""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function

__version__ = VERSION

class ModeratorAgent(BaseAgent):
    """Agent for reviewing content for safety, tone, and policy compliance."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are a Content Moderator and Senior Reviewer. "
            "Your task is to analyze the provided content for toxic language, bias, "
            "safety violations, and adherence to professional tone and style guides. "
            "Flag potential issues and provide objective feedback for improvement."
        )

    def _get_default_content(self) -> str:
        return "# Moderation Review\n\n- No content provided for review yet.\n"

if __name__ == "__main__":
    main = create_main_function(ModeratorAgent, "Moderator Agent", "File to review for moderation")
    main()