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

"""
Copilot cli backend.py module.
"""


from __future__ import annotations

import logging
import subprocess

from src.core.base.lifecycle.version import VERSION

from .llm_backend import LLMBackend

__version__ = VERSION


class CopilotCliBackend(LLMBackend):
    """GitHub Copilot CLI LLM Backend."""

    def chat(
        self,
        prompt: str,
        model: str = "gh-extension",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        if not self._is_working("copilot_cli"):
            logging.debug("Copilot CLI skipped due to connection cache.")
            return ""

        timeout_s = kwargs.get("timeout_s", 30)
        import time

        start_t = time.time()
        try:
            # Phase 141 Fix: Windows command line length limit (WinError 206)
            # gh copilot suggest doesn't need the full strategic roadmap, just a task summary.
            # Phase 317 expansion: Increasing to 4000 to allow more context for code fixes.
            max_char = 4000
            safe_prompt = prompt[:max_char] + "..." if len(prompt) > max_char else prompt

            # We use 'shell' type because suggest works best with it,
            # though it's still far from a full LLM.
            cmd = ["gh", "copilot", "suggest", "-t", "shell", safe_prompt]
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, encoding="utf-8")
            latency = time.time() - start_t

            if process.returncode == 0:
                content = process.stdout.strip()

                # Phase 317 Protection: Detecting gh-copilot deprecation message
                if "gh-copilot extension has been deprecated" in content:
                    logging.warning("Copilot CLI detected deprecation message. Skipping backend.")
                    self._update_status("copilot_cli", False)
                    return ""

                self._record(
                    "copilot_cli",
                    model,
                    safe_prompt,
                    content,
                    system_prompt=system_prompt,
                    latency_s=latency,
                )
                self._update_status("copilot_cli", True)
                return content
            else:
                logging.debug(f"Copilot CLI error: {process.stderr}")
                self._update_status("copilot_cli", False)
                self._record(
                    "copilot_cli",
                    model,
                    safe_prompt,
                    f"ERROR: {process.stderr}",
                    system_prompt=system_prompt,
                    latency_s=latency,
                )
                return ""
        except Exception as e:
            latency = time.time() - start_t
            logging.error(f"Failed to call Copilot CLI: {e}")
            self._update_status("copilot_cli", False)
            self._record(
                "copilot_cli",
                model,
                prompt[:100],
                f"ERROR: {str(e)}",
                system_prompt=system_prompt,
                latency_s=latency,
            )
            return ""
