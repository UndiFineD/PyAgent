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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Agent specializing in Bash and shell scripting."""




from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.utilities import create_main_function
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

