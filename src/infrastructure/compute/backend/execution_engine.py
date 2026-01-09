#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""Multi-backend execution engine with fallback and caching capabilities."""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports
import requests
import subprocess
from src.classes.backend import *

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

def get_metrics() -> Dict[str, Any]:
    """Get current metrics snapshot."""
    return _runner.get_metrics()

def reset_metrics() -> None:
    """Reset metrics."""
    _runner.reset_metrics()

def validate_response_content(response: str, content_types: Optional[List[str]] = None) -> bool:
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
    base_url: Optional[str] = None,
    token: Optional[str] = None,
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

def run_subagent(description: str, prompt: str, original_content: str = "") -> Optional[str]:
    """Run a subagent."""
    return _runner.run_subagent(description, prompt, original_content)

def get_backend_status() -> Dict[str, Any]:
    """Return diagnostic snapshot."""
    return _runner.get_backend_status()

def describe_backends() -> str:
    """Return human-readable diagnostics."""
    return _runner.describe_backends()
