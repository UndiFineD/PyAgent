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


"""Agent specializing in Go (Golang) programming."""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.development.coder_agent import CoderAgent
from src.core.base.common.base_utilities import create_main_function

__version__ = VERSION


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
        return 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, Go!")\n}\n'


if __name__ == "__main__":
    main = create_main_function(GoAgent, "Go Agent", "Path to Go file (.go)")
    main()
