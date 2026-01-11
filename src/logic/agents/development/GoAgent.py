#!/usr/bin/env python3

"""Agent specializing in Go (Golang) programming."""

from __future__ import annotations

from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.utilities import create_main_function
import logging

class GoAgent(CoderAgent):
    """Agent for Go code improvement and auditing."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "go"
        self._system_prompt = (
            "You are a Go Expert. "
            "Focus on concurrency patterns (goroutines, channels), "
            "effective error handling, interface design, and idiomatic Go project structure. "
            "Follow 'Effective Go' principles."
        )

    def _get_default_content(self) -> str:
        return "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello, Go!\")\n}\n"

if __name__ == "__main__":
    main = create_main_function(GoAgent, "Go Agent", "Path to Go file (.go)")
    main()


