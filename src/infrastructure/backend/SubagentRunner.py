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

"""Implementation of subagent running logic."""

from __future__ import annotations
from src.core.base.version import VERSION
import hashlib
import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from .DiskCache import DiskCache
from .LLMClient import LLMClient
from .LocalContextRecorder import LocalContextRecorder
from .SubagentCore import SubagentCore
from .SubagentStatus import SubagentStatus

__version__ = VERSION

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]

class SubagentRunner:
    """Handles running subagents with multiple backend support and fallback logic."""
    
    _command_cache: dict[str, bool] = {}

    @staticmethod
    def _resolve_repo_root() -> Path:
        """Resolve the repository root directory (Phase 108)."""
        env_root = os.environ.get("DV_AGENT_REPO_ROOT")
        if env_root:
            return Path(env_root).expanduser().resolve()
        here = Path(__file__).resolve()
        for parent in [here.parent, *here.parents]:
            if (parent / ".git").exists():
                return parent
        return Path.cwd()

    @staticmethod
    def _command_available(command: str) -> bool:
        """Check if a command is available in PATH with result caching (Phase 108)."""
        if command in SubagentRunner._command_cache:
            return SubagentRunner._command_cache[command]
            
        try:
            logging.debug(f"Checking if command is available: {command}")
            # Use 'which' on Linux/Mac or 'where' on Windows for faster checks
            subprocess.run(
                ['where' if os.name == 'nt' else 'which', command],
                capture_output=True,
                text=True,
                timeout=2,
                check=True,
            )
            logging.debug(f"Command available: {command}")
            SubagentRunner._command_cache[command] = True
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            logging.debug(f"Command not available: {command}")
            SubagentRunner._command_cache[command] = False
            return False

    def __init__(self) -> None:
        """Initialize the subagent runner with empty cache and metrics."""
        self._response_cache: dict[str, str] = {}
        
        # Disk cache initialization
        repo_root = self._resolve_repo_root()
        self.disk_cache = DiskCache(repo_root / ".agent_cache", ttl_seconds=60*60*24*7) # 7 days default
        
        # Phase 108: Recording Intelligence
        self.recorder = LocalContextRecorder(workspace_root=repo_root)
        
        self._metrics: dict[str, Any] = {
            "requests": 0,
            "errors": 0,
            "timeouts": 0,
            "cache_hits": 0,
            "total_latency_ms": 0,
        }
        self._requests = requests
        self._llm_client = LLMClient(requests)
        self._core = SubagentCore(self)
        self._status_manager = SubagentStatus(self)

    @property
    def requests(self) -> bool:
        return self._requests

    @requests.setter
    def requests(self, value: Any) -> None:
        self._requests = value
        # Refresh LLMClient when requests lib changes (e.g. during testing)
        self._llm_client = LLMClient(value)

    @property
    def llm_client(self) -> LLMClient:
        return self._llm_client

    @llm_client.setter
    def llm_client(self, value: LLMClient) -> None:
        self._llm_client = value

    def record_interaction(self, provider: str, model: str, prompt: str, result: str, meta: dict[str, Any] = None) -> None:
        """Record an interaction for intelligence harvesting (Phase 108)."""
        if self.recorder:
            self.recorder.record_interaction(provider, model, prompt, result, meta=meta)

    def clear_response_cache(self) -> None:
        """Clear the response cache."""
        self._response_cache.clear()
        if hasattr(self, 'disk_cache'):
            self.disk_cache.clear()
        logging.debug("Response cache cleared")

    def get_metrics(self) -> dict[str, Any]:
        """Get current metrics snapshot."""
        return {k: v for k, v in self._metrics.items()}

    def reset_metrics(self) -> None:
        """Reset metrics to zero."""
        self._metrics.update({
            "requests": 0,
            "errors": 0,
            "timeouts": 0,
            "cache_hits": 0,
            "total_latency_ms": 0,
        })
        logging.debug("Metrics reset")

    def _get_cache_key(self, prompt: str, model: str) -> str:
        """Generate a cache key for a prompt-model combination."""
        content = f"{prompt}:{model}".encode()
        return hashlib.sha256(content).hexdigest()

    def validate_response_content(self, response: str, content_types: list[str] | None = None) -> bool:
        """Validate that AI response contains expected content types."""
        if not response:
            return False
        response_lower = response.lower()
        if not content_types:
            return bool(response.strip())
        for content_type in content_types:
            if content_type.lower() in response_lower:
                return True
        logging.warning(f"Response validation failed: expected {content_types}, got partial match")
        return True

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        if not text:
            return 0
        return max(1, len(text) // 4)

    def estimate_cost(self, tokens: int, model: str = "gpt-4", rate_per_1k_input: float = 0.03) -> float:
        """Estimate cost for API-based backends."""
        cost = (tokens / 1000.0) * rate_per_1k_input
        logging.debug(f"Estimated cost for {tokens} tokens: ${cost:.6f}")
        return cost

    def configure_timeout_per_backend(self, backend: str, timeout_s: int) -> None:
        """Configure timeout for specific backend type."""
        env_key = f"DV_AGENT_TIMEOUT_{backend.upper()}"
        os.environ[env_key] = str(timeout_s)
        logging.debug(f"Configured {backend} timeout to {timeout_s}s")

    def llm_chat_via_github_models(
        self,
        prompt: str,
        model: str,
        **kwargs: Any
    ) -> str:
        """Call a GitHub Models OpenAI-compatible chat endpoint with caching."""
        return self._core.llm_chat_via_github_models(prompt, model, **kwargs)

    def _looks_like_command(self, text: str) -> bool:
        """Helper to decide if a prompt is command-like."""
        t = (text or "").strip()
        if not t:
            return False
        if "\n" in t:
            return False
        if any(op in t for op in ("|", "&&", ";")):
            return True
        starters = ("git ", "gh ", "docker ", "kubectl ", "pip ", "python ", "npm ", "node ", "pwsh ", "powershell ", "Get-", "Set-", "New-")
        return t.startswith(starters)

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str | None:
        """Run a subagent using available backends."""
        return self._core.run_subagent(description, prompt, original_content)

    def llm_chat_via_ollama(self, *args, **kwargs) -> str:
        """Proxy to LLMClient."""
        return self.llm_client.llm_chat_via_ollama(*args, **kwargs)

    def llm_chat_via_vllm(self, *args, **kwargs) -> str:
        """Proxy to LLMClient."""
        return self.llm_client.llm_chat_via_vllm(*args, **kwargs)

    def get_backend_status(self) -> dict[str, Any]:
        """Return diagnostic snapshot of backend availability."""
        return self._status_manager.get_backend_status()

    def describe_backends(self) -> str:
        """Return human-readable backend diagnostics."""
        return self._status_manager.describe_backends()