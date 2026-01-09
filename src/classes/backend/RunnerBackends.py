#!/usr/bin/env python3

"""Backend implementation handlers for SubagentRunner."""

from __future__ import annotations

import logging
import os
import subprocess
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

class BackendHandlers:
    """Namespace for backend execution logic."""

    @staticmethod
    def build_full_prompt(description: str, prompt: str, original_content: str) -> str:
        try:
            max_context_chars = int(os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000"))
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
    def try_codex_cli(full_prompt: str, repo_root: Path, recorder=None) -> Optional[str]:
        try:
            logging.debug("Attempting to use Codex CLI backend")
            result = subprocess.run(
                ['codex', '--prompt', full_prompt, '--no-color', '--log-level', 'error', '--add-dir', str(repo_root),
                 '--allow-all-tools', '--disable-parallel-tools-execution', '--deny-tool', 'write', '--deny-tool', 'shell',
                 '--silent', '--stream', 'off'],
                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180, cwd=str(repo_root), check=False
            )
            stdout = (result.stdout or "").strip()
            
            # Phase 108: Recording
            if recorder:
                recorder.record_interaction("codex", "cli", full_prompt[:200], stdout[:1000] if result.returncode == 0 else "FAILED")

            if result.returncode == 0 and stdout:
                logging.info("Codex CLI backend succeeded")
                return stdout
            if result.returncode != 0:
                logging.debug(f"Codex CLI failed (code {result.returncode}): {result.stderr}")
        except subprocess.TimeoutExpired:
            logging.warning("Codex CLI timed out")
        except Exception as e:
            logging.warning(f"Codex CLI error: {e}")
        return None

    @staticmethod
    def try_copilot_cli(full_prompt: str, repo_root: Path) -> Optional[str]:
        try:
            logging.debug("Attempting to use local Copilot CLI backend")
            result = subprocess.run(
                ['copilot', 'explain', full_prompt],
                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60, cwd=str(repo_root), check=False
            )
            stdout = (result.stdout or "").strip()
            if result.returncode == 0 and stdout:
                logging.info("Copilot CLI backend succeeded")
                return stdout
        except Exception as e:
            logging.warning(f"Copilot CLI error: {e}")
        return None

    @staticmethod
    def try_gh_copilot(full_prompt: str, repo_root: Path, allow_non_command: bool = False) -> Optional[str]:
        # Optimization: if not a command and not allowed, skip
        if not allow_non_command:
             # Basic heuristic: if it doesn't look like a command, skip gh copilot explain
             # (This logic was partially in SubagentRunner, but we can pass a flag)
             pass

        try:
            logging.debug("Attempting to use gh copilot alias backend")
            # Note: gh copilot requires interactive session or specific config for shell completion
            # We attempt it as a subprocess call
            result = subprocess.run(
                ['gh', 'copilot', 'explain', full_prompt],
                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60, cwd=str(repo_root), check=False
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
        except Exception as e:
            logging.debug(f"gh copilot failed: {e}")
        return None

    @staticmethod
    def try_github_models(full_prompt: str, requests_lib: Any) -> Optional[str]:
        if not requests_lib:
            return None
        
        base_url = (os.environ.get("GITHUB_MODELS_BASE_URL") or "https://models.inference.ai.azure.com").strip().rstrip("/")
        model = (os.environ.get("DV_AGENT_MODEL") or os.environ.get("GITHUB_MODELS_MODEL") or "gpt-4o-mini").strip()
        
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            search_paths = [
                os.environ.get("DV_GITHUB_TOKEN_FILE"),
                r"C:\DEV\github-gat.txt",
                "github-token.txt"
            ]
            for path_str in search_paths:
                if not path_str:
                    continue
                path = Path(path_str)
                if path.exists():
                    try:
                        token = path.read_text(encoding='utf-8').strip()
                        if token:
                            break
                    except Exception:
                        continue
        
        if not token:
            logging.debug("GitHub Models skipped: No token found")
            return None

        logging.debug(f"Attempting GitHub Models (model: {model})")
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                "model": model,
                "temperature": 0.1,
                "max_tokens": 4096
            }
            response = requests_lib.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.warning(f"GitHub Models error: {e}")
            return None

    @staticmethod
    def try_openai_api(full_prompt: str, requests_lib: Any) -> Optional[str]:
        if not requests_lib:
            return None
            
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        model = os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"
        
        if not api_key:
            logging.debug("OpenAI API skipped: No API key")
            return None

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0
            }
            response = requests_lib.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.warning(f"OpenAI API error: {e}")
            return None

