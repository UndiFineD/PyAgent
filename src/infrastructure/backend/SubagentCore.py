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

"""Core execution logic for SubagentRunner."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import os
import time
from typing import Optional, TYPE_CHECKING
from .RunnerBackends import BackendHandlers

__version__ = VERSION

if TYPE_CHECKING:
    from .SubagentRunner import SubagentRunner

class SubagentCore:
    """Delegated execution core for SubagentRunner."""
    
    def __init__(self, runner: SubagentRunner) -> None:
        self.runner = runner

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str | None:
        """Run a subagent using available backends."""
        backend_env = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
        use_cache = os.environ.get("DV_AGENT_CACHE", "true").lower() == "true"
        
        cache_model = backend_env if backend_env != "auto" else "subagent_auto"
        cache_key = self.runner._get_cache_key(f"{description}:{prompt}:{original_content}", cache_model)

        if use_cache:
            if cache_key in self.runner._response_cache:
                self.runner._metrics["cache_hits"] += 1
                return self.runner._response_cache[cache_key]
            cached_val = self.runner.disk_cache.get(cache_key)
            if cached_val:
                self.runner._metrics["cache_hits"] += 1
                self.runner._response_cache[cache_key] = cached_val
                return cached_val

        full_prompt = BackendHandlers.build_full_prompt(description, prompt, original_content)
        repo_root = self.runner._resolve_repo_root()

        def _try_codex_cli() -> str | None:
            if not self.runner._command_available('codex'):
                return None
            return BackendHandlers.try_codex_cli(full_prompt, repo_root)

        def _try_copilot_cli() -> str | None:
            if not self.runner._command_available('copilot'):
                return None
            return BackendHandlers.try_copilot_cli(full_prompt, repo_root)

        def _try_gh_copilot(allow_non_command: bool) -> str | None:
            if not self.runner._command_available('gh'):
                return None
            if not allow_non_command and not self.runner._looks_like_command(prompt):
                return None
            return BackendHandlers.try_gh_copilot(full_prompt, repo_root, allow_non_command)

        def _try_github_models() -> str | None:
            return BackendHandlers.try_github_models(full_prompt, self.runner.requests)

        def _try_vllm() -> str | None:
            return self.runner.llm_client.llm_chat_via_vllm(full_prompt, model="llama3")

        def _try_ollama() -> str | None:
            return self.runner.llm_client.llm_chat_via_ollama(full_prompt, model="llama3")

        def _try_openai_api() -> str | None:
            return BackendHandlers.try_openai_api(full_prompt, self.runner.requests)

        res = None
        if backend_env in {"codex", "codex-cli"}:
            res = _try_codex_cli()
        elif backend_env in {"vllm"}:
            res = _try_vllm()
        elif backend_env in {"ollama"}:
            res = _try_ollama()
        elif backend_env in {"copilot", "local", "copilot-cli"}:
            res = _try_codex_cli() or _try_vllm() or _try_ollama() or _try_copilot_cli()
        elif backend_env in {"gh", "gh-copilot"}:
            res = _try_gh_copilot(allow_non_command=True)
        elif backend_env in {"github-models", "github_models", "models"}:
            res = _try_github_models()
        elif backend_env in {"openai", "gpt", "localai", "huggingface"}:
            res = _try_openai_api()
        else:
            # auto (default) logic
            res = (_try_vllm() or _try_ollama() or _try_codex_cli() or 
                   _try_copilot_cli() or _try_github_models() or 
                   _try_openai_api() or _try_gh_copilot(allow_non_command=False))

        if res and use_cache:
            self.runner._response_cache[cache_key] = res
            self.runner.disk_cache.set(cache_key, res)
        
        if self.runner.recorder:
            self.runner.recorder.record_interaction(
                provider="SubagentRunner",
                model=backend_env,
                prompt=prompt,
                result=res or "FAILED"
            )
            
        return res

    def llm_chat_via_github_models(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        base_url: str | None = None,
        token: str | None = None,
        timeout_s: int = 60,
        max_retries: int = 2,
        use_cache: bool = True,
        stream: bool = False,
        validate_content: bool = True,
    ) -> str:
        """Call a GitHub Models OpenAI-compatible chat endpoint with caching."""
        cache_key = self.runner._get_cache_key(prompt, model)
        if use_cache:
            if cache_key in self.runner._response_cache:
                self.runner._metrics["cache_hits"] += 1
                return self.runner._response_cache[cache_key]
            cached_val = self.runner.disk_cache.get(cache_key)
            if cached_val:
                self.runner._metrics["cache_hits"] += 1
                self.runner._response_cache[cache_key] = cached_val
                return cached_val

        self.runner._metrics["requests"] += 1
        start_time = time.time()
        try:
            result = self.runner.llm_client.llm_chat_via_github_models(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                base_url=base_url,
                token=token,
                timeout_s=timeout_s,
                max_retries=max_retries,
                stream=stream
            )
            
            if result:
                if validate_content and not self.runner.validate_response_content(result):
                    logging.warning("Response validation failed")
                if use_cache:
                    self.runner._response_cache[cache_key] = result
                    self.runner.disk_cache.set(cache_key, result)
                latency_ms = int((time.time() - start_time) * 1000)
                self.runner._metrics["total_latency_ms"] += latency_ms
                return result
            return ""
        except Exception as e:
            self.runner._metrics["errors"] += 1
            logging.error(f"GitHub Models call failed: {e}")
            raise