#!/usr/bin/env python3

"""Agent specializing in Rust programming."""

from __future__ import annotations

from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.utilities import create_main_function
import logging

class RustAgent(CoderAgent):
    """Agent for Rust code improvement and auditing."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "rust"
        self._system_prompt = (
            "You are a Rust Expert. "
            "Focus on memory safety, ownership patterns, idiomatic usage of Result/Option, "
            "zero-cost abstractions, and effective use of the borrow checker. "
            "Suggest crates from crates.io where appropriate for common tasks."
        )

    def _get_default_content(self) -> str:
        return 'fn main() {\n    println!("Hello, Rust!");\n}\n'

if __name__ == "__main__":
    main = create_main_function(RustAgent, "Rust Agent", "Path to Rust file (.rs)")
    main()


