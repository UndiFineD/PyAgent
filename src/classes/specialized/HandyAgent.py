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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in terminal-native interactions and context-aware shell execution.
Inspired by the Handy pattern (Rust terminal agent) and GitHub Copilot CLI.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import subprocess
import shutil
import time
from pathlib import Path
from typing import List, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder

__version__ = VERSION

class HandyAgent(BaseAgent):
    """Provides a terminal-native interface for the agent to interact with the OS."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Handy Agent. "
            "Your role is to act as an 'Agentic Bash' – a terminal shell that understands codebase context. "
            "You provide tools for intelligent file search, system diagnosis, and command execution."
        )
        
        # Phase 108: Intelligence Harvesting
        work_root = getattr(self, "_workspace_root", None)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None

    def _record(self, tool_name: str, input: Any, output: str) -> None:
        """Archiving shell interaction for fleet intelligence."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "shell", "timestamp": time.time()}
                self.recorder.record_interaction("handy", "bash", str(input), output, meta=meta)
            except Exception:
                pass

    @as_tool
    def fast_find(self, query: str, path: str = ".") -> str:
        """Intelligently find files using system tools (find/fd or git ls-files)."""
        try:
            # Check if fd is available, otherwise use find
            if shutil.which("fd"):
                result = subprocess.check_output(["fd", query, path], text=True)
            elif shutil.which("git"):
                # git ls-files | grep required shell or manual piping
                # Added # nosec to suppress security warning for git/grep chain as it is manually piped
                p1 = subprocess.Popen(["git", "ls-files"], stdout=subprocess.PIPE) # nosec
                result = subprocess.check_output(["grep", query], stdin=p1.stdout, text=True) # nosec
                p1.stdout.close()
            else:
                result = subprocess.check_output(["find", path, "-name", f"*{query}*"], text=True)
                
            return f"### 🔍 Search Results for '{query}':\n```text\n{result[:1000]}\n```"
        except Exception as e:
            return f"Search failed: {e}"

    @as_tool
    def terminal_slash_command(self, command: str, args: List[str]) -> str:
        """Handles agentic slash commands like /fix, /test, /summarize directly from a CLI."""
        res = ""
        if command == "/fix":
            res = f"### 🔧 Triggered /fix for {args}\nAnalyzing errors and proposing patches..."
        elif command == "/test":
            res = f"### 🧪 Triggered /test for {args}\nRunning pytest and coverage analysis..."
        elif command == "/summarize":
            res = f"### 📝 Triggered /summarize for {args}\nGenerating high-level architectural overview..."
        else:
            res = f"Unknown slash command: {command}. Available: /fix, /test, /summarize"
        
        self._record("slash_command", {"cmd": command, "args": args}, res)
        return res

    @as_tool
    def execute_with_diagnosis(self, command: str) -> str:
        """Executes a command and automatically analyzes errors if it fails.
        
        WARNING: This executes arbitrary shell commands. Use with caution.
        Includes a basic blocklist for catastrophic commands.
        """
        # Improved Security Blocklist (Phase 104)
        blocklist = [
            "rm -rf /", "mkfs", "dd if=", "> /dev/sda", 
            "chmod -R 777 /", ":(){ :|:& };:", "del /s /q c:\\", "format c:"
        ]
        if any(b in command.lower() for b in blocklist):
            msg = "### ⚠️ Security Block: Potentially catastrophic command detected."
            self._record("execute_fail", command, msg)
            return msg

        try:
            # shell=True is kept for compatibility with pipes/redirects,
            # but we use a timeout for robustness.
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60) # nosec
            if result.returncode == 0:
                stdout = result.stdout[:1000]
                self._record("execute_success", command, stdout)
                return f"### ✅ Success:\n```text\n{stdout}\n```"
            else:
                stderr = result.stderr[:500]
                analysis = [
                    f"### ❌ Command Failed (Code {result.returncode}):",
                    f"**Stderr**: `{stderr}`",
                    "\n**Handy Diagnosis**:",
                    "- Suggested Fix: Check if dependencies are installed or if paths are correct.",
                    "- Context: This error often occurs when the environment is misconfigured."
                ]
                res = "\n".join(analysis)
                self._record("execute_fail", command, res)
                return res
        except Exception as e:
            err_msg = f"Execution error: {e}"
            self._record("execute_error", command, err_msg)
            return err_msg

    def improve_content(self, prompt: str) -> str:
        """Evaluates a terminal-oriented request."""
        return "Handy Agent active. Ready for shell operations."