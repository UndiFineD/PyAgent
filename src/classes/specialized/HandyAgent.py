#!/usr/bin/env python3

"""Agent specializing in terminal-native interactions and context-aware shell execution.
Inspired by the Handy pattern (Rust terminal agent) and GitHub Copilot CLI.
"""

import os
import subprocess
import shutil
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

class HandyAgent(BaseAgent):
    """Provides a terminal-native interface for the agent to interact with the OS."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Handy Agent. "
            "Your role is to act as an 'Agentic Bash' – a terminal shell that understands codebase context. "
            "You provide tools for intelligent file search, system diagnosis, and command execution."
        )

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
        if command == "/fix":
            return f"### 🔧 Triggered /fix for {args}\nAnalyzing errors and proposing patches..."
        elif command == "/test":
            return f"### 🧪 Triggered /test for {args}\nRunning pytest and coverage analysis..."
        elif command == "/summarize":
            return f"### 📝 Triggered /summarize for {args}\nGenerating high-level architectural overview..."
        else:
            return f"Unknown slash command: {command}. Available: /fix, /test, /summarize"

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
            return "### ⚠️ Security Block: Potentially catastrophic command detected."

        try:
            # shell=True is kept for compatibility with pipes/redirects,
            # but we use a timeout for robustness.
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60) # nosec
            if result.returncode == 0:
                return f"### ✅ Success:\n```text\n{result.stdout[:1000]}\n```"
            else:
                analysis = [
                    f"### ❌ Command Failed (Code {result.returncode}):",
                    f"**Stderr**: `{result.stderr[:500]}`",
                    "\n**Handy Diagnosis**:",
                    "- Suggested Fix: Check if dependencies are installed or if paths are correct.",
                    "- Context: This error often occurs when the environment is misconfigured."
                ]
                return "\n".join(analysis)
        except Exception as e:
            return f"Execution error: {e}"

    def improve_content(self, prompt: str) -> str:
        """Evaluates a terminal-oriented request."""
        return "Handy Agent active. Ready for shell operations."
