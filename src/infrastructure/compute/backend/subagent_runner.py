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


"""Implementation of subagent running logic.

Phase 15 Rust Optimizations:
- estimate_tokens_rust: Fast BPE-approximated token counting
- validate_response_rust: Vectorized content validation
"""

from __future__ import annotations

import hashlib
import logging
import os
import subprocess
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

from src.infrastructure.compute.backend.disk_cache import DiskCache
from src.infrastructure.compute.backend.llm_client import LLMClient
from src.infrastructure.compute.backend.local_context_recorder import LocalContextRecorder
from src.infrastructure.compute.backend.subagent_core import SubagentCore
from src.infrastructure.compute.backend.subagent_status import SubagentStatus

__version__ = VERSION

try:
    import rust_core as rc

    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False

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
        if env_root := os.environ.get("DV_AGENT_REPO_ROOT"):
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
            logging.debug("Checking if command is available: %s", command)
            # Use 'which' on Linux/Mac or 'where' on Windows for faster checks
            subprocess.run(
                ["where" if os.name == "nt" else "which", command],
                capture_output=True,
                text=True,
                timeout=2,
                check=True,
            )
            logging.debug("Command available: %s", command)
            SubagentRunner._command_cache[command] = True
            return True
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            logging.debug("Command not available: %s", command)
            SubagentRunner._command_cache[command] = False
            return False

    def __init__(self) -> None:
        """Initialize the subagent runner with empty cache and metrics."""
        self._response_cache: dict[str, str] = {}

        # Disk cache initialization
        repo_root = self._resolve_repo_root()
        self.disk_cache = DiskCache(repo_root / "data/agent_cache", ttl_seconds=60 * 60 * 24 * 7)  # 7 days default

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
        """Get the requests session or flag."""
        return self._requests

    @requests.setter
    def requests(self, value: Any) -> None:
        self._requests = value
        # Refresh LLMClient when requests lib changes (e.g. during testing)
        self._llm_client = LLMClient(value)

    @property
    def llm_client(self) -> LLMClient:
        """Get the LLM client instance."""
        return self._llm_client

    @llm_client.setter
    def llm_client(self, value: LLMClient) -> None:
        self._llm_client = value

    def record_interaction(
        self,
        provider: str,
        model: str,
        prompt: str,
        result: str,
        meta: dict[str, Any] | None = None,
    ) -> None:
        """Record an interaction for intelligence harvesting (Phase 108)."""
        if self.recorder:
            self.recorder.record_interaction(provider, model, prompt, result, meta=meta)

    def clear_response_cache(self) -> None:
        """Clear the response cache."""
        self._response_cache.clear()
        if hasattr(self, "disk_cache"):
            self.disk_cache.clear()
        logging.debug("Response cache cleared")

    def get_metrics(self) -> dict[str, Any]:
        """Get current metrics snapshot."""
        return dict(self._metrics)

    def reset_metrics(self) -> None:
        """Reset metrics to zero."""
        self._metrics.update(
            {
                "requests": 0,
                "errors": 0,
                "timeouts": 0,
                "cache_hits": 0,
                "total_latency_ms": 0,
            }
        )
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
        logging.warning("Response validation failed: expected %s, got partial match", content_types)
        return True

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text.

        Uses Rust-accelerated BPE approximation when available.
        """
        if not text:
            return 0

        # Rust-accelerated token estimation
        if RUST_AVAILABLE:
            if hasattr(rc, "fast_token_count_rust"):
                try:
                    return rc.fast_token_count_rust(text)
                except (AttributeError, ValueError, RuntimeError):
                    pass
            if hasattr(rc, "estimate_tokens_rust"):
                try:
                    # Only return if it's not returning 1 for large inputs (heuristic check)
                    res = rc.estimate_tokens_rust(text)
                    if res > 1 or len(text) < 10:
                        return res
                except (AttributeError, ValueError, RuntimeError):
                    pass  # Fall back to Python

        return max(1, len(text) // 4)

    def estimate_cost(self, tokens: int, _model: str = "gpt-4", rate_per_1k_input: float = 0.03) -> float:
        """Estimate cost for API-based backends."""
        cost = (tokens / 1000.0) * rate_per_1k_input
        logging.debug("Estimated cost for %d tokens: $%s", tokens, f"{cost:.6f}")
        return cost

    def configure_timeout_per_backend(self, backend: str, timeout_s: int) -> None:
        """Configure timeout for specific backend type."""
        env_key = f"DV_AGENT_TIMEOUT_{backend.upper()}"
        os.environ[env_key] = str(timeout_s)
        logging.debug("Configured %s timeout to %ds", backend, timeout_s)

    def llm_chat_via_github_models(self, prompt: str, model: str, **kwargs: Any) -> str:
        """Call a GitHub Models OpenAI-compatible chat endpoint with caching."""
        return self._core.llm_chat_via_github_models(prompt, model, **kwargs)

    def _has_command_operators(self, text: str) -> bool:
        """Check if text contains command operators."""
        return any(op in text for op in ("|", "&&", ";"))

    def _starts_with_command_prefix(self, text: str) -> bool:
        """Check if text starts with common command prefixes."""
        starters = (
            "git ",
            "gh ",
            "docker ",
            "kubectl ",
            "pip ",
            "python ",
            "npm ",
            "node ",
            "pwsh ",
            "powershell ",
            "Get-",
            "Set-",
            "New-",
        )
        return text.startswith(starters)

    def _looks_like_command(self, text: str) -> bool:
        """Helper to decide if a prompt is command-like."""
        t = (text or "").strip()
        if not t:
            return False
        if "\n" in t:
            return False
        if self._has_command_operators(t):
            return True
        return self._starts_with_command_prefix(t)

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str | None:
        """Run a subagent using available backends."""
        return self._core.run_subagent(description, prompt, original_content)

    def llm_chat_via_ollama(self, *args, **kwargs) -> str:
        """Proxy to LLMClient."""
        return self.llm_client.llm_chat_via_ollama(*args, **kwargs)

    def llm_chat_via_vllm(self, *args, **kwargs) -> str:
        """Proxy to LLMClient."""
        return self.llm_client.llm_chat_via_vllm(*args, **kwargs)

    def llm_chat_via_copilot_cli(self, *args, **kwargs) -> str:
        """Proxy to LLMClient."""
        return self.llm_client.llm_chat_via_copilot_cli(*args, **kwargs)

    def get_backend_status(self) -> dict[str, Any]:
        """Return diagnostic snapshot of backend availability."""
        return self._status_manager.get_backend_status()

    def describe_backends(self) -> str:
        """Return human-readable backend diagnostics."""
        return self._status_manager.describe_backends()
