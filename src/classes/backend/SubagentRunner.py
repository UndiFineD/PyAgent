#!/usr/bin/env python3

"""Implementation of subagent running logic."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .DiskCache import DiskCache
from .RunnerBackends import BackendHandlers
from .LLMClient import LLMClient

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]


class SubagentRunner:
    """Handles running subagents with multiple backend support and fallback logic."""
    
    _command_cache: Dict[str, bool] = {}

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
        self._response_cache: Dict[str, str] = {}
        
        # Disk cache initialization
        repo_root = self._resolve_repo_root()
        self.disk_cache = DiskCache(repo_root / ".agent_cache", ttl_seconds=60*60*24*7) # 7 days default
        
        self._metrics: Dict[str, Any] = {
            "requests": 0,
            "errors": 0,
            "timeouts": 0,
            "cache_hits": 0,
            "total_latency_ms": 0,
        }
        self.requests = requests
        self.llm_client = LLMClient(requests)

    def clear_response_cache(self) -> None:
        """Clear the response cache."""
        self._response_cache.clear()
        if hasattr(self, 'disk_cache'):
            self.disk_cache.clear()
        logging.debug("Response cache cleared")

    def get_metrics(self) -> Dict[str, Any]:
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
        content = f"{prompt}:{model}".encode('utf-8')
        return hashlib.sha256(content).hexdigest()

    def validate_response_content(self, response: str, content_types: Optional[List[str]] = None) -> bool:
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
        system_prompt: str = "You are a helpful assistant.",
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout_s: int = 60,
        max_retries: int = 2,
        use_cache: bool = True,
        stream: bool = False,
        validate_content: bool = True,
    ) -> str:
        """Call a GitHub Models OpenAI-compatible chat endpoint with caching."""
        cache_key = self._get_cache_key(prompt, model)
        if use_cache:
            if cache_key in self._response_cache:
                self._metrics["cache_hits"] += 1
                return self._response_cache[cache_key]
            cached_val = self.disk_cache.get(cache_key)
            if cached_val:
                self._metrics["cache_hits"] += 1
                self._response_cache[cache_key] = cached_val
                return cached_val

        self._metrics["requests"] += 1
        start_time = time.time()
        try:
            result = self.llm_client.llm_chat_via_github_models(
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
                if validate_content and not self.validate_response_content(result):
                    logging.warning("Response validation failed")
                if use_cache:
                    self._response_cache[cache_key] = result
                    self.disk_cache.set(cache_key, result)
                latency_ms = int((time.time() - start_time) * 1000)
                self._metrics["total_latency_ms"] += latency_ms
                return result
            return ""
        except Exception as e:
            self._metrics["errors"] += 1
            logging.error(f"GitHub Models call failed: {e}")
            raise

    def _looks_like_command(self, text: str) -> bool:
        """Helper to decide if a prompt is command-like."""
        t = (text or "").strip()
        if not t: return False
        if "\n" in t: return False
        if any(op in t for op in ("|", "&&", ";")): return True
        starters = ("git ", "gh ", "docker ", "kubectl ", "pip ", "python ", "npm ", "node ", "pwsh ", "powershell ", "Get-", "Set-", "New-")
        return t.startswith(starters)

    def run_subagent(self, description: str, prompt: str, original_content: str = "") -> Optional[str]:
        """Run a subagent using available backends."""
        backend_env = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
        use_cache = os.environ.get("DV_AGENT_CACHE", "true").lower() == "true"
        
        cache_model = backend_env if backend_env != "auto" else "subagent_auto"
        cache_key = self._get_cache_key(f"{description}:{prompt}:{original_content}", cache_model)

        if use_cache:
            if cache_key in self._response_cache:
                self._metrics["cache_hits"] += 1
                return self._response_cache[cache_key]
            cached_val = self.disk_cache.get(cache_key)
            if cached_val:
                self._metrics["cache_hits"] += 1
                self._response_cache[cache_key] = cached_val
                return cached_val

        full_prompt = BackendHandlers.build_full_prompt(description, prompt, original_content)
        repo_root = self._resolve_repo_root()

        def _try_codex_cli() -> Optional[str]:
            if not self._command_available('codex'): return None
            return BackendHandlers.try_codex_cli(full_prompt, repo_root)

        def _try_copilot_cli() -> Optional[str]:
            if not self._command_available('copilot'): return None
            return BackendHandlers.try_copilot_cli(full_prompt, repo_root)

        def _try_gh_copilot(allow_non_command: bool) -> Optional[str]:
            if not self._command_available('gh'): return None
            if not allow_non_command and not self._looks_like_command(prompt): return None
            return BackendHandlers.try_gh_copilot(full_prompt, repo_root, allow_non_command)

        def _try_github_models() -> Optional[str]:
            return BackendHandlers.try_github_models(full_prompt, self.requests)

        def _try_vllm() -> Optional[str]:
            return self.llm_client.llm_chat_via_vllm(full_prompt, model="llama3")

        def _try_ollama() -> Optional[str]:
            return self.llm_client.llm_chat_via_ollama(full_prompt, model="llama3")

        def _try_openai_api() -> Optional[str]:
            return BackendHandlers.try_openai_api(full_prompt, self.requests)

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
            # auto (default) logic: Priority on local high-performance backends (Phase 108)
            res = _try_vllm() or _try_ollama() or _try_codex_cli() or _try_copilot_cli() or _try_github_models() or _try_openai_api() or _try_gh_copilot(allow_non_command=False)

        if res and use_cache:
            self._response_cache[cache_key] = res
            self.disk_cache.set(cache_key, res)
            
        return res

    def llm_chat_via_ollama(self, *args, **kwargs) -> str:
        """Proxy to LLMClient."""
        return self.llm_client.llm_chat_via_ollama(*args, **kwargs)

    def llm_chat_via_vllm(self, *args, **kwargs) -> str:
        """Proxy to LLMClient."""
        return self.llm_client.llm_chat_via_vllm(*args, **kwargs)

    def get_backend_status(self) -> Dict[str, Any]:
        """Return diagnostic snapshot of backend availability."""
        backend = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
        repo_root = str(self._resolve_repo_root())
        try:
            max_context_chars = int(os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000"))
        except ValueError:
            max_context_chars = 12_000
        models_base_url = (os.environ.get("GITHUB_MODELS_BASE_URL") or "").strip()
        models_model = (os.environ.get("DV_AGENT_MODEL") or os.environ.get("GITHUB_MODELS_MODEL") or "").strip()
        
        token_set = bool(os.environ.get("GITHUB_TOKEN"))
        if not token_set:
            token_file = os.environ.get("DV_GITHUB_TOKEN_FILE", r"C:\DEV\github-gat.txt")
            token_set = Path(token_file).exists()

        warnings = []
        if os.environ.get("TERM_PROGRAM") == "vscode":
            warnings.append("VS Code Environment: Pylance or Git extensions may lock files or cause rewrite conflicts.")
        if os.name == 'nt':
            warnings.append("Windows Platform: Sensitive to file locks. Consider closing open editors for target files.")

        return {
            "selected_backend": backend,
            "repo_root": repo_root,
            "max_context_chars": max_context_chars,
            "warnings": warnings,
            "commands": {
                "codex": self._command_available("codex"),
                "copilot": self._command_available("copilot"),
                "gh": self._command_available("gh"),
            },
            "github_models": {
                "requests_installed": self.requests is not None,
                "base_url_set": bool(models_base_url),
                "model_set": bool(models_model),
                "token_set": token_set,
                "configured": bool(models_base_url and models_model and token_set and self.requests is not None),
            },
        }

    def describe_backends(self) -> str:
        """Return human-readable backend diagnostics."""
        status = self.get_backend_status()
        cmd = status["commands"]
        models = status["github_models"]
        def yn(v: bool) -> str: return "yes" if v else "no"
        
        lines = [
            "Backend diagnostics:",
            f"- selected: {status['selected_backend']}",
            f"- repo_root: {status['repo_root']}",
            f"- max_context_chars: {status['max_context_chars']}",
            f"- codex CLI available: {yn(bool(cmd.get('codex')))}",
            f"- local copilot CLI available: {yn(bool(cmd.get('copilot')))}",
            f"- gh CLI available: {yn(bool(cmd.get('gh')))}",
            "- github-models configured:",
            f"  - requests installed: {yn(bool(models.get('requests_installed')))}",
            f"  - base_url set: {yn(bool(models.get('base_url_set')))}",
            f"  - model set: {yn(bool(models.get('model_set')))}",
            f"  - token set: {yn(bool(models.get('token_set')))}",
        ]
        
        if status.get("warnings"):
            lines.append("- POTENTIAL CONFLICTS:")
            for w in status["warnings"]:
                lines.append(f"  ! {w}")
                
        return "\n".join(lines)
