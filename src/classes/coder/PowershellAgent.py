#!/usr/bin/env python3

"""Agent specializing in PowerShell scripting."""

from .CoderAgent import CoderAgent
from src.classes.base_agent.utilities import create_main_function
import logging

class PowershellAgent(CoderAgent):
    """Agent for PowerShell scripts."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "powershell"
        self._system_prompt = (
            "You are an Expert PowerShell Scripter. "
            "Focus on idiomatic PowerShell, proper naming conventions (Verb-Noun), "
            "error handling (Try/Catch), and pipeline efficiency."
        )

    def _get_default_content(self) -> str:
        return "# PowerShell Script\nWrite-Host 'Hello World'\n"

if __name__ == "__main__":
    main = create_main_function(PowershellAgent, "PowerShell Agent", "Path to .ps1 file")
    main()

