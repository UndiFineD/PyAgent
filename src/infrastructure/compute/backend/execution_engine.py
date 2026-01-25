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


"""Multi-backend execution engine with fallback and caching capabilities."""

# pylint: disable=protected-access

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import requests

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.compute.backend.subagent_runner import SubagentRunner

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports

__version__ = VERSION

# Shared runner instance for functional compatibility
_runner = SubagentRunner()

# Expose internal state for compatibility with legacy tests
_response_cache = _runner._response_cache
_metrics = _runner._metrics


def _resolve_repo_root() -> Path:
    """Legacy helper."""

    return _runner._resolve_repo_root()


def _command_available(command: str) -> bool:
    """Legacy helper."""

    return _runner._command_available(command)


def _get_cache_key(prompt: str, model: str) -> str:
    """Legacy helper."""
    return _runner._get_cache_key(prompt, model)


def clear_response_cache() -> None:
    """Clear the response cache."""
    _runner.clear_response_cache()


def get_metrics() -> dict[str, Any]:
    """Get current metrics snapshot."""
    return _runner.get_metrics()


def reset_metrics() -> None:
    """Reset metrics."""
    _runner.reset_metrics()


def validate_response_content(response: str, content_types: list[str] | None = None) -> bool:
    """Validate AI response content."""
    return _runner.validate_response_content(response, content_types)


def estimate_tokens(text: str) -> int:
    """Estimate token count."""
    return _runner.estimate_tokens(text)


def estimate_cost(tokens: int, model: str = "gpt-4", rate_per_1k_input: float = 0.03) -> float:
    """Estimate cost."""
    return _runner.estimate_cost(tokens, model, rate_per_1k_input)


def configure_timeout_per_backend(backend: str, timeout_s: int) -> None:
    """Configure timeout."""
    _runner.configure_timeout_per_backend(backend, timeout_s)


def llm_chat_via_github_models(
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
    """Call GitHub Models chat endpoint."""
    # Ensure any monkey-patching of 'requests' in this module propagates to the runner
    _runner.requests = requests
    return _runner.llm_chat_via_github_models(
        prompt=prompt,
        model=model,
        system_prompt=system_prompt,
        base_url=base_url,
        token=token,
        timeout_s=timeout_s,
        max_retries=max_retries,
        use_cache=use_cache,
        stream=stream,
        validate_content=validate_content,
    )


def llm_chat_via_ollama(_prompt: str) -> str | None:
    """Call local Ollama endpoint (Phase 112 placeholder)."""
    return None


def llm_chat_via_copilot_cli(_prompt: str) -> str | None:
    """Call Copilot CLI endpoint (Phase 112 placeholder)."""
    return None


def run_subagent(description: str, prompt: str, original_content: str = "") -> str | None:
    """Run a subagent."""
    return _runner.run_subagent(description, prompt, original_content)


def get_backend_status() -> dict[str, Any]:
    """Return diagnostic snapshot."""
    return _runner.get_backend_status()


def describe_backends() -> str:
    """Return human-readable diagnostics."""
    return _runner.describe_backends()
