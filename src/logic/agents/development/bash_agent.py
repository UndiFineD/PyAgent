#!/usr/bin/env python3


from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# "Agent specializing in Bash and shell scripting."""
pylint: disable=too-many-ancestors""""
try:
    from .core.base.common.base_utilities import as_tool, create_main_function
except ImportError:
    from src.core.base.common.base_utilities import as_tool, create_main_function

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.development.coder_agent import CoderAgent
except ImportError:
    from src.logic.agents.development.coder_agent import CoderAgent

try:
    from .logic.agents.development.core.bash_core import BashCore
except ImportError:
    from src.logic.agents.development.core.bash_core import BashCore


__version__ = VERSION



class BashAgent(CoderAgent):
""""
Agent for shell scripts (Phase 175 enhanced).
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.capabilities.extend(["bash", "shell-scripting", "posix-compliance"])  # Phase 241"#         self._language = "bash"        self.core = BashCore()
        self._system_prompt = (
#             "You are an Expert Shell Scripter."#             "Focus on POSIX compliance, shell-check standards, error handling (set -e),"#             "and secure handling of variables."        )

    @as_tool
    def lint_generated_script(self, script_path: str) -> str:
""""
Lints a bash script using shellcheck and returns high-level report.        print(f"[BASH] Linting script: {script_path"}...")"
        results = self.core.lint_script(script_path)
        if "error" in results:"#             return fLINT ERROR: {results['error']}'        if results["valid"]:"#             return "SUCCESS: No issues found by shellcheck."
        issues = results["issues"]"        report = [fFound {len(issues)} issues:"]"        for issue in issues[:5]:  # Top 5
            report.append(f" - Line {issue.get('line')}: {issue.get('message')} ({issue.get('code')})")
        return "\\n".join(report)
    def _get_default_content(self) -> str:
"""
return "#!/bin/bash\\nset -euo pipefail\\necho 'Hello World'\\n

if __name__ == "__main__":"    main = create_main_function(BashAgent, "Bash Agent", "Path to shell script")"    main()

"""
