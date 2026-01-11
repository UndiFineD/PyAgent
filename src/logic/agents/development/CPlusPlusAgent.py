#!/usr/bin/env python3

"""Agent specializing in C++ programming."""

from __future__ import annotations

from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.utilities import create_main_function
import logging

class CPlusPlusAgent(CoderAgent):
    """Agent for C++ code improvement and auditing."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "cpp"
        self._system_prompt = (
            "You are a C++ Expert. "
            "Focus on modern C++ (C++11/14/17/20/23) features, "
            "RAII, smart pointers, template metaprogramming, and performance optimization. "
            "Ensure low-latency and memory-efficient patterns are used."
        )

    def _get_default_content(self) -> str:
        return "#include <iostream>\n\nint main() {\n    std::cout << 'Hello, C++!' << std::endl;\n    return 0;\n}\n"

if __name__ == "__main__":
    main = create_main_function(CPlusPlusAgent, "C++ Agent", "Path to C++ file (.cpp, .hpp, .cc)")
    main()


