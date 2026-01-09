#!/usr/bin/env python3

"""Agent specializing in Bash and shell scripting."""

from .CoderAgent import CoderAgent
from src.classes.base_agent.utilities import create_main_function
import logging

class BashAgent(CoderAgent):
    """Agent for shell scripts."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "bash"
        self._system_prompt = (
            "You are an Expert Shell Scripter. "
            "Focus on POSIX compliance, shell-check standards, error handling (set -e), "
            "and secure handling of variables."
        )

    def _get_default_content(self) -> str:
        return "#!/bin/bash\nset -euo pipefail\necho 'Hello World'\n"

if __name__ == "__main__":
    main = create_main_function(BashAgent, "Bash Agent", "Path to shell script")
    main()

