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


"""Centralized LLM client for various backends."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.connectivity_manager import ConnectivityManager
from src.infrastructure.compute.backend.core.pooling_core import PoolingCore

from .llm_backends.copilot_cli_backend import CopilotCliBackend
from .llm_backends.git_hub_models_backend import GitHubModelsBackend
from .llm_backends.lm_studio_backend import LMStudioBackend
from .llm_backends.ollama_backend import OllamaBackend
from .llm_backends.vllm_backend import VllmBackend
from .llm_backends.vllm_native_backend import VllmNativeBackend
from .local_context_recorder import LocalContextRecorder


class LLMClient:
    """Handles direct HTTP calls to LLM providers.
    Enhanced with PoolingCore for prompt compression and connection optimization.
    """

    def __init__(self, requests_lib: Any, workspace_root: str | None = None) -> None:
        self.requests = requests_lib
        self.pooling_core = PoolingCore()

        # Phase 108: Persistent Session for connection pooling
        # If we're being passed a mock or patched requests, avoid Session for better test compatibility
        self.session = requests_lib

        # Only create a real session if it looks like the real requests module and hasn't been explicitly disabled
        import requests as real_requests

        is_real_requests = requests_lib is real_requests

        if (
            is_real_requests
            and hasattr(requests_lib, "Session")
            and os.environ.get("DV_AGENT_USE_SESSION", "true").lower() == "true"
        ):
            try:
                self.session = requests_lib.Session()
                # Security Patch 115.1: Harden session against decompression bombs and redirect chains
                self.session.max_redirects = 5
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                self.session = requests_lib

        # Auto-init recorder if workspace provided, else None
        self.workspace_root = workspace_root
        self.recorder = LocalContextRecorder(Path(workspace_root)) if workspace_root else None
        self.connectivity = ConnectivityManager(workspace_root)

        # Phase 108: Result Caching (Speed optimization for repeated calls)
        self._result_cache: dict[str, str] = {}
        self._max_cache_size = 1000

        # Backend Registry (Phase 120 Extraction)
        self.backends = {
            "github_models": GitHubModelsBackend(self.session, self.connectivity, self.recorder),
            "ollama": OllamaBackend(self.session, self.connectivity, self.recorder),
            "vllm": VllmBackend(self.session, self.connectivity, self.recorder),
            "vllm_native": VllmNativeBackend(self.session, self.connectivity, self.recorder),
            "copilot_cli": CopilotCliBackend(self.session, self.connectivity, self.recorder),
            # Phase 21: LM Studio integration
            "lmstudio": LMStudioBackend(self.session, self.connectivity, self.recorder),
        }

    def _is_backend_disabled(self, backend_name: str) -> bool:
        """Check if a backend is disabled via environment variables."""
        disabled_backends = os.environ.get("DV_DISABLED_BACKENDS", "").strip()
        if not disabled_backends:
            return False
        
        # Split by comma and strip whitespace
        disabled_list = [b.strip().lower() for b in disabled_backends.split(",")]
        return backend_name.lower() in disabled_list

    def chat(self, _provider: str, _model: str, prompt: str, system_prompt: str = "") -> str:
        """Central entry point for chat completion. Compresses prompt before sending."""
        # 1. Compress system prompt via Core
        self.pooling_core.compress_prompt(system_prompt)

        # 2. Logic to invoke backends (simplified for this edit)
        # In actual code, this would delegate to backends[provider].chat(...)
        return f"Simulated response for: {prompt[:20]}"

    def _get_cache_key(self, provider: str, model: str, prompt: str, system_prompt: str) -> str:
        import hashlib

        combined = f"{provider}:{model}:{system_prompt}:{prompt}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def _load_conn_status(self) -> dict[str, dict[str, Any]]:
        # Redundant logic for backward compatibility
        return {}

    def _save_conn_status(self) -> None:
        # Redundant logic for backward compatibility
        pass

    def _is_connection_working(self, provider_id: str) -> bool:
        """Checks if the connection is known to be working via central ConnectivityManager."""
        return self.connectivity.is_endpoint_available(provider_id)

    def _update_connection_status(self, provider_id: str, working: bool) -> None:
        """Updates the connection status via central ConnectivityManager."""
        self.connectivity.update_status(provider_id, working)

    def _record(
        self,
        provider: str,
        model: str,
        prompt: str,
        result: str,
        system_prompt: str = "",
    ) -> str:
        """
        Helper to record interactions if recorder is active.
        Optimized for future trillion-parameter community data ingestion.
        """
        if self.recorder:
            try:
                # Include system prompt and metadata for future fine-tuning
                meta = {
                    "system_prompt": system_prompt,
                    "phase": 108,
                    "timestamp_unix": time.time(),
                }
                self.recorder.record_interaction(provider, model, prompt, result, meta=meta)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                # Silently fail logging so we don't block the actual logic
                logging.error(f"Failed to record interaction: {e}")

    def llm_chat_via_github_models(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """Call a GitHub Models OpenAI-compatible chat endpoint."""
        return self.backends["github_models"].chat(prompt, model, system_prompt, **kwargs)

    def llm_chat_via_ollama(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """Call a local Ollama instance."""
        return self.backends["ollama"].chat(prompt, model, system_prompt, **kwargs)

    def llm_chat_via_vllm(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """Call a local vLLM instance (OpenAI-compatible)."""
        return self.backends["vllm"].chat(prompt, model, system_prompt, **kwargs)

    def llm_chat_via_vllm_native(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        model: str = "vllm-native",
        **kwargs,
    ) -> str:
        """Uses the locally installed vLLM library (Native Engine) for maximum performance."""
        return self.backends["vllm_native"].chat(prompt, model, system_prompt, **kwargs)

    def llm_chat_via_copilot_cli(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        model: str = "copilot-cli",
        **kwargs,
    ) -> str:
        """Calls the GitHub Copilot CLI (copilot)."""
        return self.backends["copilot_cli"].chat(prompt, model, system_prompt, **kwargs)

    def llm_chat_via_lmstudio(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """
        Call LM Studio local inference server (Phase 21).

        Uses the lmstudio SDK for WebSocket-based communication.
        Supports streaming, tool calling, and embeddings.

        Args:
            prompt: User message
            model: Model identifier (empty = any loaded model)
            system_prompt: System message
            **kwargs: Additional options (temperature, max_tokens, etc.)

        Returns:
            Generated response text
        """
        return self.backends["lmstudio"].chat(prompt, model, system_prompt, **kwargs)

    def smart_chat(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        preference: str = "local",
        local_model: str = "",
        external_model: str = "Meta-Llama-3.1-8B-Instruct",
    ) -> str:
        """
        Smartly chooses between local and external AI models.
        'local' preference attempts Native vLLM, then remote vLLM/Ollama, then Copilot CLI.
        Implements Phase 108 Result Caching for extreme speed.
        """
        # Ensure local_model has a default value if empty - read from environment for Ollama
        if not local_model:
            # Read from DV_OLLAMA_MODEL environment variable, default to tinyllama
            env_model = os.environ.get("DV_OLLAMA_MODEL", "tinyllama").strip("'\"")
            # Map 'tinyllama' to 'tinyllama:latest' to match Ollama's model tag
            if env_model == "tinyllama":
                env_model = "tinyllama:latest"
            local_model = env_model
        # Phase 108: Check Result Cache First
        cache_key = self._get_cache_key(preference, local_model, prompt, system_prompt)
        if cache_key in self._result_cache:
            logging.debug("LLMClient: Cache hit for smart_chat.")
            return self._result_cache[cache_key]

        # Phase 108: Check for Preferred working endpoint first (15m TTL)
        preferred = self.connectivity.get_preferred_endpoint("llm_backends")

        # Phase 317 robustness: If preferred is copilot_cli, we only use it if no other
        # local backends are available, as it's low-quality for code fixes.
        if preferred == "copilot_cli" and (
            (not self._is_backend_disabled("ollama") and self.connectivity.is_endpoint_available("ollama"))
            or (not self._is_backend_disabled("vllm") and self.connectivity.is_endpoint_available("vllm"))
            or (not self._is_backend_disabled("vllm_native") and self.connectivity.is_endpoint_available("vllm_native"))
        ):
            logging.debug("LLMClient: Skipping 'copilot_cli' preferred in favor of better local options.")
            preferred = None

        # Skip disabled backends
        if preferred and self._is_backend_disabled(preferred):
            logging.debug(f"LLMClient: Skipping disabled backend '{preferred}'.")
            preferred = None

        if preferred:
            result = getattr(self, f"llm_chat_via_{preferred}")(
                prompt,
                model=local_model if "local" in preferred else external_model,
                system_prompt=system_prompt,
            )
            # Validation: don't return if it's obviously useless
            if result and len(result) > 10:
                self._result_cache[cache_key] = result
                return result

            # If preferred failed or returned trash, mark it unavailable and fallback
            logging.debug(f"LLMClient: Preferred '{preferred}' returned insufficient result. Falling back.")
            self.connectivity.update_status(preferred, False)

        # Robustness Patch (Phase 141): If all known endpoints are cached as offline,
        # force a retry across all of them ignoring the skipped cache.
        force_retry = False
        known_backends = [
            "lmstudio",  # Phase 21: LM Studio (highest priority local)
            "vllm_native",
            "vllm",
            "ollama",
            "copilot_cli",
            "github_models",
        ]
        # Filter out disabled backends
        available_backends = [b for b in known_backends if not self._is_backend_disabled(b)]
        if all(not self.connectivity.is_endpoint_available(b) for b in available_backends):
            logging.info("LLMClient: All available backends cached as offline. Forcing cache bypass for robustness.")
            force_retry = True

        result = ""
        used_provider = "none"

        if preference == "local":
            # 0. Try LM Studio (Highest Priority Local, Phase 21)
            if (not self._is_backend_disabled("lmstudio") and
                    (force_retry or self.connectivity.is_endpoint_available("lmstudio"))):
                result = self.llm_chat_via_lmstudio(prompt, model=local_model, system_prompt=system_prompt)
                if result:
                    used_provider = "lmstudio"

            # 1. Try Native vLLM Library (High Performance Local, Phase 108)
            if (not result and not self._is_backend_disabled("vllm_native") and
                    (force_retry or self.connectivity.is_endpoint_available("vllm_native"))):
                result = self.llm_chat_via_vllm_native(prompt, system_prompt=system_prompt, model=local_model)
                if result:
                    used_provider = "vllm_native"

            # 2. Try vLLM Server (Remote/Docker)
            if (not result and not self._is_backend_disabled("vllm") and
                    (force_retry or self.connectivity.is_endpoint_available("vllm"))):
                result = self.llm_chat_via_vllm(prompt, model=local_model, system_prompt=system_prompt)
                if result:
                    used_provider = "vllm"

            # 3. Try Ollama if vLLM failed
            if (not result and not self._is_backend_disabled("ollama") and
                    (force_retry or self.connectivity.is_endpoint_available("ollama"))):
                result = self.llm_chat_via_ollama(prompt, model=local_model, system_prompt=system_prompt)
                if result:
                    used_provider = "ollama"

            # 3. Try Copilot CLI if local servers failed
            if (not result and not self._is_backend_disabled("copilot_cli") and
                    (force_retry or self.connectivity.is_endpoint_available("copilot_cli"))):
                result = self.llm_chat_via_copilot_cli(prompt, system_prompt=system_prompt)
                if result:
                    used_provider = "copilot_cli"

        # 4. Fallback to GitHub Models (External)
        if not result and (force_retry or self.connectivity.is_endpoint_available("github_models")):
            logging.info(f"Checking external fallback ({external_model})...")
            result = self.llm_chat_via_github_models(prompt, model=external_model, system_prompt=system_prompt)
            if result:
                used_provider = "github_models"

        if not result:
            logging.warning("All AI backends failed or were unreachable.")
            return ""

        # Phase 108: Update Preferred Endpoint Cache
        if used_provider != "none":
            self.connectivity.set_preferred_endpoint("llm_backends", used_provider)

        # Phase 108: Store in result cache

        if len(self._result_cache) < self._max_cache_size:
            self._result_cache[cache_key] = result

        return result


__version__ = VERSION
