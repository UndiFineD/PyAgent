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

"""
Moderator Agent - Content moderation and policy compliance

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Run as a script to review a single file for moderation issues:
    python moderator_agent.py <path-to-file-to-review>
Or import ModeratorAgent in automation and instantiate with a file path to perform programmatic reviews.

WHAT IT DOES:
- Subclasses BaseAgent to provide a focused moderation reviewer agent.
- Establishes a system prompt tuned for content moderation, toxicity/bias detection,
  safety violations, and professional tone feedback.
- Supplies a sensible default content template when no input is provided and wires a
  CLI entrypoint via create_main_function for single-file reviews.

FILE CONTENT SUMMARY:
Agent specializing in moderation, review, and policy compliance.
"""

from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

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

    async def _process_task(self, task_data: dict) -> dict:
        """Process a moderation review task asynchronously."""
        review_result = self.run(task_data.get("content", self._get_default_content()))
        return {"review": review_result}


if __name__ == "__main__":
    main = create_main_function(ModeratorAgent, "Moderator Agent", "File to review for moderation")
    main()
