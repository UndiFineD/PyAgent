#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/backend/RunnerBackends.description.md

# RunnerBackends

**File**: `src\classes\backend\RunnerBackends.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 232  
**Complexity**: 7 (moderate)

## Overview

Backend implementation handlers for SubagentRunner.

## Classes (1)

### `BackendHandlers`

Namespace for backend execution logic.

**Methods** (7):
- `_parse_content(text)`
- `build_full_prompt(description, prompt, original_content)`
- `try_codex_cli(full_prompt, repo_root, recorder)`
- `try_copilot_cli(full_prompt, repo_root)`
- `try_gh_copilot(full_prompt, repo_root, allow_non_command)`
- `try_github_models(full_prompt, requests_lib)`
- `try_openai_api(full_prompt, requests_lib)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `src.core.base.version.VERSION`
- `subprocess`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/backend/RunnerBackends.improvements.md

# Improvements for RunnerBackends

**File**: `src\classes\backend\RunnerBackends.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 232 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RunnerBackends_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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


"""Backend implementation handlers for SubagentRunner."""

from src.core.base.version import VERSION
import logging
import os
import subprocess
import asyncio
import json
import re
from pathlib import Path
from typing import Any, Optional

__version__ = VERSION


class BackendHandlers:
    """Namespace for backend execution logic."""

    @staticmethod
    def _parse_content(text: str) -> Any:
        if "[IMAGE_DATA:" not in text:
            return text

        parts = []
        # Find [IMAGE_DATA:base64]
        pattern = r"\[IMAGE_DATA:([^\]\s]+)\]"
        last_idx = 0
        for match in re.finditer(pattern, text):
            pre_text = text[last_idx : match.start()].strip()
            if pre_text:
                parts.append({"type": "text", "text": pre_text})

            image_data = match.group(1)
            if not image_data.startswith("data:image"):
                image_data = f"data:image/png;base64,{image_data}"

            parts.append({"type": "image_url", "image_url": {"url": image_data}})
            last_idx = match.end()

        remaining = text[last_idx:].strip()
        if remaining:
            parts.append({"type": "text", "text": remaining})

        return parts if parts else text

    @staticmethod
    def build_full_prompt(description: str, prompt: str, original_content: str) -> str:
        """Constructs the full prompt for backends."""
        try:
            max_context_chars = int(
                os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000")
            )
        except ValueError:
            max_context_chars = 12_000
        trimmed_original = (original_content or "")[:max_context_chars]
        return (
            f"Task: {description}\\n\\n"
            f"Prompt:\\n{prompt}\\n\\n"
            "Context (existing file content):\\n"
            f"{trimmed_original}"
        ).strip()

    @staticmethod
    async def try_codex_cli(
        full_prompt: str, repo_root: Path, recorder=None
    ) -> str | None:
        """Attempts to use the Codex CLI backend, with robust error handling and recording."""
        try:
            logging.debug("Attempting to use Codex CLI backend")
            process = await asyncio.create_subprocess_exec(
                "codex",
                "--prompt",
                full_prompt,
                "--no-color",
                "--log-level",
                "error",
                "--add-dir",
                str(repo_root),
                "--allow-all-tools",
                "--disable-parallel-tools-execution",
                "--deny-tool",
                "write",
                "--deny-tool",
                "shell",
                "--silent",
                "--stream",
                "off",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(repo_root),
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=180
                )
            except asyncio.TimeoutError:
                process.kill()
                raise
            stdout = stdout.decode("utf-8", errors="replace").strip()
            returncode = process.returncode
            # Phase 108: Recording
            if recorder:
                output = stdout[:1000] if returncode == 0 else "FAILED"
                recorder.record_interaction("codex", "cli", full_prompt[:200], output)

            if returncode == 0 and stdout:
                logging.info("Codex CLI backend succeeded")
                return stdout
            if returncode != 0:
                stderr_msg = stderr.decode("utf-8", errors="replace") if stderr else ""
                logging.debug(f"Codex CLI failed (code {returncode}): {stderr_msg}")
        except asyncio.TimeoutError:
            logging.warning("Codex CLI timed out")
        except Exception as e:
            logging.warning(f"Codex CLI error: {e}")
        return None

    @staticmethod
    async def try_copilot_cli(full_prompt: str, repo_root: Path) -> str | None:
        """Attempts to use the Copilot CLI backend, with robust error handling."""
        try:
            logging.debug("Attempting to use local Copilot CLI backend")
            process = await asyncio.create_subprocess_exec(
                "copilot",
                "explain",
                full_prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(repo_root),
            )
            try:
                stdout, _ = await asyncio.wait_for(process.communicate(), timeout=60)
            except asyncio.TimeoutError:
                process.kill()
                raise
            stdout = stdout.decode("utf-8", errors="replace").strip()
            if process.returncode == 0 and stdout:
                logging.info("Copilot CLI backend succeeded")
                return stdout
        except Exception as e:
            logging.warning(f"Copilot CLI error: {e}")
        return None

    @staticmethod
    async def try_gh_copilot(
        full_prompt: str, repo_root: Path, allow_non_command: bool = False
    ) -> str | None:
        """Attempts to use the gh copilot alias backend for code explanation.

        Args:
            full_prompt: The prompt to send to gh copilot.
            repo_root: The root directory of the repository.
            allow_non_command: Whether to allow non-command prompts (unused optimization flag).

        Returns:
            The response from gh copilot, or None if the call fails.
        """
        # Optimization: if not a command and not allowed, skip
        if not allow_non_command:
            # Basic heuristic: if it doesn't look like a command, skip gh copilot explain
            # (This logic was partially in SubagentRunner, but we can pass a flag)
            pass

        try:
            logging.debug("Attempting to use gh copilot alias backend")
            # Note: gh copilot requires interactive session or specific config for shell completion
            # We attempt it as a subprocess call
            process = await asyncio.create_subprocess_exec(
                "gh",
                "copilot",
                "explain",
                full_prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(repo_root),
            )
            try:
                stdout, _ = await asyncio.wait_for(process.communicate(), timeout=60)
            except asyncio.TimeoutError:
                process.kill()
                raise
            if process.returncode == 0 and stdout:
                return stdout.decode("utf-8", errors="replace").strip()
        except Exception as e:
            logging.debug(f"gh copilot failed: {e}")
        return None

    @staticmethod
    def try_github_models(full_prompt: str, requests_lib: Any) -> str | None:
        """Attempts to use the GitHub Models API backend for code generation.

        Args:
            full_prompt: The prompt to send to the GitHub Models API.
            requests_lib: The requests library instance for making HTTP calls.

        Returns:
            The response from GitHub Models, or None if the call fails or token is not found.
        """
        if not requests_lib:
            return None

        base_url = (
            (
                os.environ.get("GITHUB_MODELS_BASE_URL")
                or "https://models.inference.ai.azure.com"
            )
            .strip()
            .rstrip("/")
        )
        model = (
            os.environ.get("DV_AGENT_MODEL")
            or os.environ.get("GITHUB_MODELS_MODEL")
            or "gpt-4o-mini"
        ) or ""
        model = model if isinstance(model, str) else ""
        model = model.strip()

        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            search_paths = [
                os.environ.get("DV_GITHUB_TOKEN_FILE"),
                r"C:\DEV\github-gat.txt",
                "github-token.txt",
            ]
            for path_str in search_paths:
                if not path_str:
                    continue
                path = Path(path_str)
                if path.exists():
                    try:
                        token = path.read_text(encoding="utf-8").strip()
                        if token:
                            break
                    except Exception:
                        continue

        if not token:
            logging.debug("GitHub Models skipped: No token found")
            return None

        logging.debug(f"Attempting GitHub Models (model: {model})")
        try:
            content = BackendHandlers._parse_content(full_prompt)
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful coding assistant.",
                    },
                    {"role": "user", "content": content},
                ],
                "model": model,
                "temperature": 0.1,
                "max_tokens": 4096,
            }
            url = f"{base_url}/v1/chat/completions"
            response = requests_lib.post(
                url, headers=headers, data=json.dumps(payload), timeout=120
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            # Lowered logging level for fallback-friendly behavior (Phase 123)
            logging.debug(f"GitHub Models error: {e}")
            return None

    @staticmethod
    def try_openai_api(full_prompt: str, requests_lib: Any) -> str | None:
        """Attempts to use the OpenAI API backend for code generation.

        Args:
            full_prompt: The prompt to send to the OpenAI API.
            requests_lib: The requests library instance for making HTTP calls.

        Returns:
            The response from OpenAI, or None if the call fails or API key is not found.
        """
        if not requests_lib:
            return None

        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        model = os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"

        if not api_key:
            logging.debug("OpenAI API skipped: No API key")
            return None

        try:
            content = BackendHandlers._parse_content(full_prompt)
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": content},
                ],
                "temperature": 0,
            }
            response = requests_lib.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.warning(f"OpenAI API error: {e}")
            return None
