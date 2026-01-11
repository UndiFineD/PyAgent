#!/usr/bin/env python3

"""Agent specializing in moderation, review, and policy compliance."""

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function
import logging

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
