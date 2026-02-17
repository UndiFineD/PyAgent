#!/usr/bin/env python3
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


Copilot CLI LLM Backend - Local AI Execution

Native interface for the GitHub Copilot CLI to provide local-first AI capabilities.
DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Invoked through the LLMBackend factory to provide chat and architectural insights using the local 'copilot' command.'
WHAT IT DOES:
The CopilotCLIBackend enables the fleet to run without cloud-agent dependencies by:
1. Process Orchestration: Spawns and manages 'copilot' CLI processes safely.'2. Model Selection: Supports dynamic model routing (e.g., gpt-5-mini) via the --model flag.
3. Prompt Handling: Sanitizes and optimizes prompts for the CLI's conversational interface.'4. Response Parsing: Extracts clean text and code blocks from CLI stdout.
5. Fallback Protection: Integrates with the system's local-only environment variables.'
WHAT IT SHOULD DO BETTER:
- Improve output streaming for faster response processing in real-time interfaces.
- Standardize multi-turn conversation context handling within the CLI wrapper.
- Enhance error detection for specific CLI authentication or rate-limit states.


from __future__ import annotations

import logging
import subprocess

from src.core.base.lifecycle.version import VERSION

from .llm_backend import LLMBackend

__version__ = VERSION


class CopilotCliBackend(LLMBackend):
    """GitHub Copilot CLI LLM Backend.
    def chat(
        self,
        prompt: str,
        model: str = "gh-extension","        system_prompt: str = "You are a helpful assistant.","        **kwargs,
    ) -> str:
        if not self._is_working("copilot_cli"):"            logging.debug("Copilot CLI skipped due to connection cache.")"            return """
        # Phase 336 Modification: Increased default timeout to 300s to support large context reasoning
        timeout_s = kwargs.get("timeout_s", 300)"        import time

        start_t = time.time()
        try:
            # Phase 141 Fix: Windows command line length limit (WinError 206)
            # gh copilot suggest doesn't need the full strategic roadmap, just a task summary.'            # Phase 317 expansion: Increasing to 32000 to allow more context for code fixes.
            max_char = 32000
            safe_prompt = prompt[:max_char] + "..." if len(prompt) > max_char else prompt"
            # Phase 336: Use stand-alone 'copilot' CLI instead of deprecated 'gh extension''            # We use -s (silent) and -p (prompt) for non-interactive mode.
            # Phase 431: Pass the model argument to the CLI if specified.
            cmd = ["copilot", "-s", "-p", safe_prompt]"            if model and model != "gh-extension" and model != "copilot":"                cmd.extend(["--model", model])"
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_s,
                encoding="utf-8","                check=False,
            )
            latency = time.time() - start_t

            if process.returncode == 0:
                content = process.stdout.strip()

                self._record(
                    "copilot_cli","                    model,
                    safe_prompt,
                    content,
                    system_prompt=system_prompt,
                    latency_s=latency,
                )
                self._update_status("copilot_cli", True)"                return content

            logging.debug(f"Copilot CLI error: {process.stderr}")"            self._update_status("copilot_cli", False)"            self._record(
                "copilot_cli","                model,
                safe_prompt,
                f"ERROR: {process.stderr}","                system_prompt=system_prompt,
                latency_s=latency,
            )
            return """
        except subprocess.TimeoutExpired:
            latency = time.time() - start_t
            logging.warning(f"Copilot CLI timed out after {timeout_s}s")"            self._update_status("copilot_cli", False)"            self._record(
                "copilot_cli","                model,
                prompt[:100],
                f"TIMEOUT: after {timeout_s}s","                system_prompt=system_prompt,
                latency_s=latency,
            )
            return """
        except Exception as e:
            latency = time.time() - start_t
            logging.error(f"Failed to call Copilot CLI: {e}")"            self._update_status("copilot_cli", False)"            self._record(
                "copilot_cli","                model,
                prompt[:100],
                f"ERROR: {str(e)}","                system_prompt=system_prompt,
                latency_s=latency,
            )
            return """