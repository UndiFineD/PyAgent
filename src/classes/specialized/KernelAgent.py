#!/usr/bin/env python3

"""Agent specializing in OS-level operations, environment management, and system diagnosis.
Inspired by Open Interpreter and Openator.
"""

import os
import sys
import json
import shutil
import platform
import logging
import subprocess
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool
from src.classes.coder.SecurityGuardAgent import SecurityGuardAgent

class KernelAgent(BaseAgent):
    """Interacts directly with the host OS to manage environments and perform diagnostics."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.security_guard = SecurityGuardAgent(file_path + ".audit")
        self._system_prompt = (
            "You are the Kernel Agent. "
            "Your role is to manage the host environment and perform system-level tasks. "
            "You can check system resources, manage files, and execute shell commands. "
            "Always prioritize safety and verify commands before execution."
        )

    @as_tool
    def get_system_info(self) -> str:
        """Returns details about the current operating system and environment."""
        info = {
            "os": platform.system(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python_version": sys.version,
            "cwd": os.getcwd(),
            "env_vars": list(os.environ.keys())[:10]  # First 10 for brevity
        }
        return json.dumps(info, indent=2)

    @as_tool
    def check_disk_space(self, path: str = ".") -> str:
        """Checks available disk space at the specified path."""
        try:
            total, used, free = shutil.disk_usage(path)
            return f"Disk Usage for {path}: {used // (2**30)}GB used / {free // (2**30)}GB free (Total: {total // (2**30)}GB)"
        except Exception as e:
            return f"Error checking disk space: {e}"

    @as_tool
    def execute_shell(self, command: str, force: bool = False) -> str:
        """Executes a shell command and returns the output (STDOUT + STDERR).
        High-risk commands require 'force=True' as a HITL gate.
        """
        logging.warning(f"KernelAgent auditing shell command: {command}")
        
        # Security Audit (HITL Gate)
        risk_level, warning = self.security_guard.audit_command(command)
        if risk_level == "HIGH" and not force:
            return (
                f"BLOCKED: High-risk command detected.\n"
                f"Warning: {warning}\n"
                f"To execute this command, you must explicitly set 'force=True' as a Human-in-the-loop verification."
            )

        try:
            # shell=True is intentional for KernelAgent as it provides direct OS shell access.
            # Security at the agent level is managed via the security_guard HITL gate.
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30) # nosec
            output = f"STDOUT:\n{result.stdout}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"
            
            # Intelligence Harvesting (Phase 108)
            if self.recorder:
                self.recorder.record_lesson("kernel_shell_exec", {"command": command, "exit_code": result.returncode})
                
            return output
        except subprocess.TimeoutExpired:
            if self.recorder:
                self.recorder.record_lesson("kernel_shell_timeout", {"command": command})
            return "Error: Command timed out after 30 seconds."
        except Exception as e:
            if self.recorder:
                self.recorder.record_lesson("kernel_shell_error", {"command": command, "error": str(e)})
            return f"Error executing command: {e}"

    @as_tool
    def list_processes(self) -> str:
        """Lists active processes (platform dependent)."""
        if platform.system() == "Windows":
            return self.execute_shell('tasklist /FI "STATUS eq running" /FO TABLE')
        else:
            return self.execute_shell("ps aux | head -n 20")

    def improve_content(self, prompt: str) -> str:
        """Overridden to handle system-level requests."""
        return self.execute_shell(prompt)

