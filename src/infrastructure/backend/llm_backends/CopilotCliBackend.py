#!/usr/bin/env python3

from __future__ import annotations
import logging
import subprocess
from typing import Any, Dict, Optional
from .LLMBackend import LLMBackend

class CopilotCliBackend(LLMBackend):
    """GitHub Copilot CLI LLM Backend."""

    def chat(self, prompt: str, model: str = "gh-extension", system_prompt: str = "You are a helpful assistant.", **kwargs) -> str:
        if not self._is_working("copilot_cli"):
            logging.debug("Copilot CLI skipped due to connection cache.")
            return ""

        timeout_s = kwargs.get("timeout_s", 30)
        try:
            # Phase 141 Fix: Windows command line length limit (WinError 206)
            # gh copilot suggest doesn't need the full strategic roadmap, just a task summary.
            max_char = 800
            safe_prompt = prompt[:max_char] + "..." if len(prompt) > max_char else prompt
            
            cmd = ["gh", "copilot", "suggest", "-t", "shell", safe_prompt]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_s,
                encoding="utf-8"
            )
            
            if process.returncode == 0:
                content = process.stdout.strip()
                self._record("copilot_cli", model, safe_prompt, content, system_prompt=system_prompt)
                self._update_status("copilot_cli", True)
                return content
            else:
                logging.debug(f"Copilot CLI error: {process.stderr}")
                self._update_status("copilot_cli", False)
                return ""
        except Exception as e:
            logging.error(f"Failed to call Copilot CLI: {e}")
            self._update_status("copilot_cli", False)
            return ""
