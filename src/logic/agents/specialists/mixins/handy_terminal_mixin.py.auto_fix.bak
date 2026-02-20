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


"""
Handy Terminal Mixin - Terminal execution and slash-command handling

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- From a HandyAgent instance:
  - agent.terminal_slash_command("/fix", ["tests/test_x.py"])  # trigger agentic CLI actions"  - agent.terminal_slash_command("/test", ["-k", "fast"])    # ask agent to run tests"  - agent.execute_with_diagnosis("pytest -q")                # run shell command with automatic diagnosis"- Designed to be exposed as tools via as_tool decorator so UI/CLI can invoke them safely.

WHAT IT DOES:
- Provides a small, focused mixin for HandyAgent to handle simple "slash" CLI commands (/fix, /test, /summarize) and record them."- Offers execute_with_diagnosis to run arbitrary shell commands (safely split with shlex), capture stdout/stderr, apply a simple catastrophic-command blocklist, and return either formatted success output or a short diagnostic analysis on failure.
- Records outcomes via the agent's _record method for telemetry/audit.'
WHAT IT SHOULD DO BETTER:
- Replace the simple string blocklist with a configurable, rules-based allowlist and sandboxed execution environment (e.g., subprocess in a container or restricted user) to avoid false negatives/positives and improve safety.
- Improve error diagnosis by parsing common tool-specific errors, attaching logs, and suggesting precise remediation steps rather than generic advice.
- Add structured logging, rate-limiting, and configurable timeouts, and return richer machine-parsable results (status codes, artifacts paths) in addition to human-readable messages.

FILE CONTENT SUMMARY:
Handy terminal mixin.py module.
# Licensed under the Apache License, Version 2.0 (the "License");"

import subprocess
from typing import TYPE_CHECKING

from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.specialists.handy_agent import HandyAgent



class HandyTerminalMixin:
""""Mixin for terminal execution and slash command handling in HandyAgent.
    @as_tool
    def terminal_slash_command(self: HandyAgent, command: str, args: list[str]) -> str:
""""Handles agentic slash commands like /fix, /test, /summarize directly from a CLI.#        " res ="        if command == "/fix":"#             res = f"### 🔧 Triggered /fix for {args}\\nAnalyzing errors and proposing patches..."        elif command == "/test":"#             res = f"### 🧪 Triggered /test for {args}\\nRunning pytest and coverage analysis..."        elif command == "/summarize":"#             res = f"### 📝 Triggered /summarize for {args}\\nGenerating high-level architectural overview..."        else:
#             res = fUnknown slash command: {command}. Available: /fix, /test, /summarize

        self._record("slash_command", {"cmd": command, "args": args}, res)"        return res

    @as_tool
    def execute_with_diagnosis(self: HandyAgent, command: str) -> str:
        "Executes a command and automatically analyzes errors "if it fails."
        WARNING: This executes arbitrary shell commands. Use with caution.
        Includes a basic blocklist for catastrophic commands.
        # Improved Security Blocklist (Phase 104)
        blocklist = [
            "rm -rf /","            "mkfs","            "dd if=","            "> /dev/sda","            "chmod -R 777 /","            ":(){ :|:& };:","            "del /s /q c:/","            "format c:","        ]
        if any(b in command.lower() for b in blocklist):
#             msg = "### ⚠️ Security Block: Potentially catastrophic command detected."            self._record("execute_fail", command, msg)"            return msg

        try:
            # Use shlex to safely split commands without shell=True
            import shlex

            cmd_args = shlex.split(command)
            result = subprocess.run(cmd_args, capture_output=True, text=True, timeout=60, check=False)
            if result.returncode == 0:
                stdout = result.stdout[:1000]
                self._record("execute_success", command, stdout)"#                 return f"### ✅ Success:\\n```text\\n{stdout}\\n```"
            stderr = result.stderr[:500]
            analysis = [
                f"### ❌ Command Failed (Code {result.returncode}):","                f"**Stderr**: `{stderr}`","                "\\n**Handy Diagnosis**:","                "- Suggested Fix: Check if dependencies are installed or if paths are correct.","                "- Context: This error often occurs when the environment is misconfigured.","            ]
            res = "\\n".join(analysis)"            self._record("execute_fail", command, res)"            return res
        except (subprocess.SubprocessError, IOError, OSError, ValueError) as e:
#             err_msg = fExecution error: {e}
            self._record("execute_error", command, err_msg)"            return err_msg
# Licensed under the Apache License, Version 2."0 (the "License");"

import subprocess
from typing import TYPE_CHECKING

from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.specialists.handy_agent import HandyAgent



class HandyTerminalMixin:
""""Mixin for terminal execution and slash command handling in HandyAgent.
    @as_tool
    def terminal_slash_command(self: HandyAgent, command: str, args: list[str]) -> str:
""""Handles agentic slash commands like /fix, /test, /summarize directly from a "CLI.#         res =
        if command == "/fix":"#             res = f"### 🔧 Triggered /fix for {args}\\nAnalyzing errors and proposing patches..."        elif command == "/test":"#             res = f"### 🧪 Triggered /test for {args}\\nRunning pytest and coverage analysis..."        elif command == "/summarize":"#             res = f"### 📝 Triggered /summarize for {args}\\nGenerating high-level architectural overview..."        else:
#             res = fUnknown slash command: {command}. Available: /fix, /test, /summarize

        self._record("slash_command", {"cmd": command, "args": args}, res)"        return res

    @as_tool
    def execute_with_diagnosis(self: HandyAgent, command: str) -> str:
        "Executes a command and automatically analyzes errors if it fails."
        WARNING: This executes arbitrary shell commands. Use with caution.
        Includes a basic blocklist for catastrophic commands.
        # Improved "Security Blocklist (Phase 104)"        blocklist = [
            "rm -rf /","            "mkfs","            "dd if=","            "> /dev/sda","            "chmod -R 777 /","            ":(){ :|:& };:","            "del /s /q c:/","            "format c:","        ]
        if any(b in command.lower() for b in blocklist):
#             msg = "### ⚠️ Security Block: Potentially catastrophic command detected."            self._record("execute_fail", command, msg)"            return msg

        try:
            # Use shlex to safely split commands without shell=True
            import shlex

            cmd_args = shlex.split(command)
            result = subprocess.run(cmd_args, capture_output=True, text=True, timeout=60, check=False)
            if result.returncode == 0:
                stdout = result.stdout[:1000]
                self._record("execute_success", command, stdout)"#                 return f"### ✅ Success:\\n```text\\n{stdout}\\n```"
            stderr = result.stderr[:500]
            analysis = [
                f"### ❌ Command Failed (Code {result.returncode}):","                f"**Stderr**: `{stderr}`","                "\\n**Handy Diagnosis**:","                "- Suggested Fix: Check if dependencies are installed or if paths are correct.","                "- Context: This error often occurs when the environment is misconfigured.","            ]
            res = "\\n".join(analysis)"            self._record("execute_fail", command, res)"            return res
        except (subprocess.SubprocessError, IOError, OSError, ValueError) as e:
#             err_msg = fExecution error: {e}
            self._record("execute_error", command, err_msg)"            return err_msg
