#!/usr/bin/env python3

"""Centralized LLM client for various backends."""

from __future__ import annotations

import json
import logging
import time
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from .LocalContextRecorder import LocalContextRecorder

class LLMClient:
    """Handles direct HTTP calls to LLM providers."""

    def __init__(self, requests_lib: Any, workspace_root: Optional[str] = None) -> None:
        self.requests = requests_lib
        # Auto-init recorder if workspace provided, else None
        self.workspace_root = workspace_root
        self.recorder = LocalContextRecorder(Path(workspace_root)) if workspace_root else None
        self._conn_status_file = Path(workspace_root) / "logs" / "ai_connection_status.json" if workspace_root else None
        self._conn_cache_ttl = 900  # 15 minutes
        self._conn_status_cache: Dict[str, Dict[str, Any]] = self._load_conn_status()
        
        # Phase 108: Result Caching (Speed optimization for repeated calls)
        self._result_cache: Dict[str, str] = {}
        self._max_cache_size = 1000

    def _get_cache_key(self, provider: str, model: str, prompt: str, system_prompt: str) -> str:
        import hashlib
        combined = f"{provider}:{model}:{system_prompt}:{prompt}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def _load_conn_status(self) -> Dict[str, Dict[str, Any]]:
        """Loads the connection status from disk."""
        if self._conn_status_file and self._conn_status_file.exists():
            try:
                with open(self._conn_status_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_conn_status(self) -> None:
        """Saves the connection status to disk."""
        if self._conn_status_file:
            try:
                os.makedirs(self._conn_status_file.parent, exist_ok=True)
                with open(self._conn_status_file, "w") as f:
                    json.dump(self._conn_status_cache, f)
            except Exception as e:
                logging.error(f"Failed to save connection status: {e}")

    def _is_connection_working(self, provider_id: str) -> bool:
        """Checks if the connection is known to be working based on cache (15m TTL)."""
        status = self._conn_status_cache.get(provider_id)
        if status:
            elapsed = time.time() - status.get("timestamp", 0)
            if elapsed < self._conn_cache_ttl:
                is_working = status.get("working", False)
                if not is_working:
                    logging.debug(f"LLMClient: Skipping '{provider_id}' (cached offline for next {int(self._conn_cache_ttl - elapsed)}s)")
                return is_working
        return True  # Assume working if no cache or expired

    def _update_connection_status(self, provider_id: str, working: bool) -> None:
        """Updates the connection status cache and persists to disk."""
        self._conn_status_cache[provider_id] = {
            "working": working,
            "timestamp": time.time()
        }
        self._save_conn_status()

    def _record(self, provider: str, model: str, prompt: str, result: str, system_prompt: str = "") -> str:
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
                    "timestamp_unix": time.time()
                }
                self.recorder.record_interaction(provider, model, prompt, result, meta=meta)
            except Exception as e:
                # Silently fail logging so we don't block the actual logic
                logging.error(f"Failed to record interaction: {e}")

    def llm_chat_via_github_models(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout_s: int = 60,
        max_retries: int = 2,
        stream: bool = False,
    ) -> str:
        """Call a GitHub Models OpenAI-compatible chat endpoint."""
        if self.requests is None:
            raise RuntimeError("Missing dependency: install 'requests' to use GitHub Models backend")

        # Connection Cache Check (Phase 108)
        if not self._is_connection_working("github_models"):
            logging.debug("GitHub Models skipped due to connection cache.")
            return ""

        resolved_token = token or os.environ.get("GITHUB_TOKEN")
        if not resolved_token:
            # Phase 108: Priority Search for local token files
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
                        resolved_token = path.read_text(encoding="utf-8").strip()
                        if resolved_token:
                            break
                    except Exception:
                        continue

        if not resolved_token:
            logging.warning("GitHub Models: Missing token. Skipping.")
            return ""
        
        resolved_base_url = (base_url or os.environ.get("GITHUB_MODELS_BASE_URL") or "https://models.inference.ai.azure.com").strip()
        if not resolved_base_url:
            logging.warning("GitHub Models: Missing base URL. Skipping.")
            return ""
        
        url = resolved_base_url.rstrip("/") + "/v1/chat/completions"
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": stream
        }
        
        headers = {
            "Authorization": f"Bearer {resolved_token}",
            "Content-Type": "application/json",
        }
        
        for attempt in range(max_retries + 1):
            try:
                response = self.requests.post(url, headers=headers, json=payload, timeout=timeout_s)
                # If 401, don't retry - it's a token issue
                if response.status_code == 401:
                    logging.error("GitHub Models: Unauthorized (401). Check GITHUB_TOKEN.")
                    self._update_connection_status("github_models", False)
                    return ""
                
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                self._record("github_models", model, prompt, content, system_prompt=system_prompt)
                self._update_connection_status("github_models", True)
                return content
            except Exception as e:
                if attempt < max_retries:
                    logging.warning(f"GitHub Models attempt {attempt+1} failed: {e}. Retrying...")
                    time.sleep(min(2 ** attempt, 10))
                else:
                    logging.error(f"LLM call failed after {max_retries} retries: {e}")
                    self._update_connection_status("github_models", False)
                    # Record failure as a lesson for future self-improvement (Phase 108)
                    self._record("github_models", model, prompt, f"ERROR: {str(e)}", system_prompt=system_prompt)
                    return "" # Return empty rather than raising to keep the fleet moving
        return ""

    def llm_chat_via_ollama(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        base_url: str = "http://localhost:11434",
        timeout_s: int = 120,
    ) -> str:
        """Call a local Ollama instance."""
        if self.requests is None:
            raise RuntimeError("Missing dependency: install 'requests' for Ollama")
        
        # Connection Cache Check (Phase 108)
        if not self._is_connection_working("ollama"):
            logging.debug("Ollama skipped due to connection cache.")
            return ""

        url = base_url.rstrip("/") + "/api/generate"
        payload = {
            "model": model,
            "system": system_prompt,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = self.requests.post(url, json=payload, timeout=timeout_s)
            response.raise_for_status()
            content = response.json().get("response", "")
            self._record("ollama", model, prompt, content, system_prompt=system_prompt)
            self._update_connection_status("ollama", True)
            return content
        except Exception as e:
            logging.error(f"Ollama call failed: {e}")
            self._update_connection_status("ollama", False)
            # Record failure context (Phase 108)
            self._record("ollama", model, prompt, f"ERROR: {str(e)}", system_prompt=system_prompt)
            return ""

    def llm_chat_via_vllm(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        base_url: str = "http://localhost:8000",
        timeout_s: int = 60,
    ) -> str:
        """Call a local vLLM instance (OpenAI-compatible)."""
        if self.requests is None:
            raise RuntimeError("Missing dependency: install 'requests' for vLLM")
            
        # Connection Cache Check (Phase 108)
        if not self._is_connection_working("vllm"):
            logging.debug("vLLM skipped due to connection cache.")
            return ""

        url = base_url.rstrip("/") + "/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = self.requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=timeout_s)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            self._record("vllm", model, prompt, content, system_prompt=system_prompt)
            self._update_connection_status("vllm", True)
            return content
        except Exception as e:
            logging.error(f"vLLM call failed: {e}")
            self._update_connection_status("vllm", False)
            # Record failure context (Phase 108)
            self._record("vllm", model, prompt, f"ERROR: {str(e)}", system_prompt=system_prompt)
            return ""

    def llm_chat_via_vllm_native(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        model: Optional[str] = None
    ) -> str:
        """
        Uses the locally installed vLLM library (Native Engine) for maximum performance.
        Records context, prompt, and result to the local training shards (Phase 108).
        """
        try:
            from .VllmNativeEngine import VllmNativeEngine
            engine = VllmNativeEngine.get_instance(model_name=model or "meta-llama/Llama-3-8B-Instruct")
            if not engine.enabled:
                return ""
            
            result = engine.generate(prompt, system_prompt=system_prompt)
            if result:
                # Direct recording for 'Own AI' training
                self._record("vllm_native", model or engine.model_name, prompt, result, system_prompt=system_prompt)
            return result
        except Exception as e:
            logging.debug(f"vLLM Native Engine unavailable: {e}")
            return ""

    def smart_chat(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        preference: str = "local",
        local_model: str = "llama3",
        external_model: str = "gpt-4o"
    ) -> str:
        """
        Smartly chooses between local and external AI models.
        'local' preference attempts Native vLLM, then remote vLLM/Ollama.
        Implements Phase 108 Result Caching for extreme speed.
        """
        # Phase 108: Check Result Cache First
        cache_key = self._get_cache_key(preference, local_model, prompt, system_prompt)
        if cache_key in self._result_cache:
            logging.debug("LLMClient: Cache hit for smart_chat.")
            return self._result_cache[cache_key]

        result = ""
        used_provider = "none"
        used_model = "none"

        if preference == "local":
            # 0. Try Native vLLM Library (Highest Performance Local, Phase 108)
            result = self.llm_chat_via_vllm_native(prompt, system_prompt=system_prompt, model=local_model)
            if result:
                used_provider, used_model = "vllm_native", local_model

            # 1. Try vLLM Server (Remote/Docker)
            if not result:
                result = self.llm_chat_via_vllm(prompt, model=local_model, system_prompt=system_prompt)
                if result:
                    used_provider, used_model = "vllm", local_model

            # 2. Try Ollama if vLLM failed
            if not result:
                result = self.llm_chat_via_ollama(prompt, model=local_model, system_prompt=system_prompt)
                if result:
                    used_provider, used_model = "ollama", local_model

        # 3. Fallback to GitHub Models (External)
        if not result:
            logging.info(f"Checking external fallback ({external_model})...")
            result = self.llm_chat_via_github_models(prompt, model=external_model, system_prompt=system_prompt)
            if result:
                used_provider, used_model = "github_models", external_model

        if not result:
            logging.warning("All AI backends failed or were unreachable.")
            return ""

        # Phase 108: Store in result cache
        if len(self._result_cache) < self._max_cache_size:
            self._result_cache[cache_key] = result

        return result

import os

