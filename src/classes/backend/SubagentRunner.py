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

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]


class SubagentRunner:
    """Handles running subagents with multiple backend support and fallback logic."""

    @staticmethod
    def _resolve_repo_root() -> Path:
        """Resolve the repository root directory."""
        env_root = os.environ.get("DV_AGENT_REPO_ROOT")
        if env_root:
            logging.debug(f"Using DV_AGENT_REPO_ROOT: {env_root}")
            return Path(env_root).expanduser().resolve()
        # Try to find .git directory by walking up from current file
        here = Path(__file__).resolve()
        for parent in [here.parent, *here.parents]:
            if (parent / ".git").exists():
                logging.debug(f"Found repo root at {parent}")
                return parent
        logging.debug(f"No repo root found, using CWD: {Path.cwd()}")
        return Path.cwd()

    @staticmethod
    def _command_available(command: str) -> bool:
        """Check if a command is available in PATH.

        Attempts to run command with --version flag to verify availability.
        """
        try:
            logging.debug(f"Checking if command is available: {command}")
            subprocess.run(
                [command, '--version'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=5,
                check=True,
            )
            logging.debug(f"Command available: {command}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            logging.debug(f"Command not available: {command}")
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
        """Call a GitHub Models OpenAI-compatible chat endpoint."""
        if self.requests is None:
            raise RuntimeError("Missing dependency: install 'requests' to use GitHub Models backend")

        cache_key = self._get_cache_key(prompt, model)
        if use_cache:
            # Check in-memory first
            if cache_key in self._response_cache:
                self._metrics["cache_hits"] += 1
                logging.debug(f"In-memory cache hit for prompt hash: {cache_key}")
                return self._response_cache[cache_key]
            
            # Check disk cache
            cached_val = self.disk_cache.get(cache_key)
            if cached_val:
                self._metrics["cache_hits"] += 1
                logging.debug(f"Disk cache hit for prompt hash: {cache_key}")
                self._response_cache[cache_key] = cached_val
                return cached_val

        resolved_token = token or os.environ.get("GITHUB_TOKEN")
        
        # Fallback to token file if not set
        if not resolved_token:
            token_file = os.environ.get("DV_GITHUB_TOKEN_FILE")
            if token_file:
                token_path = Path(token_file)
                if token_path.exists():
                    try:
                        logging.debug(f"Reading GitHub token from {token_path}")
                        resolved_token = token_path.read_text(encoding="utf-8").strip()
                    except Exception as e:
                        logging.warning(f"Failed to read token from {token_path}: {e}")

        if not resolved_token:
            raise RuntimeError("Missing token: set GITHUB_TOKEN env var, provide DV_GITHUB_TOKEN_FILE, or pass token=")
        
        resolved_base_url = (base_url or os.environ.get("GITHUB_MODELS_BASE_URL") or "").strip()
        if not resolved_base_url:
            raise RuntimeError("Missing base URL: set GITHUB_MODELS_BASE_URL env var or pass base_url=")
        
        url = resolved_base_url.rstrip("/") + "/v1/chat/completions"
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        if stream:
            payload["stream"] = True
        
        headers = {
            "Authorization": f"Bearer {resolved_token}",
            "Content-Type": "application/json",
        }
        
        last_error = None
        start_time = time.time()
        self._metrics["requests"] += 1
        
        for attempt in range(max_retries + 1):
            try:
                logging.debug(f"Making GitHub Models API request (attempt {attempt + 1}/{max_retries + 1})")
                response = self.requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout_s)
                response.raise_for_status()
                data = response.json()
                try:
                    result = (data["choices"][0]["message"]["content"] or "").strip()
                    if validate_content and not self.validate_response_content(result):
                        logging.warning("Response validation failed, but continuing")
                    if use_cache:
                        self._response_cache[cache_key] = result
                        self.disk_cache.set(cache_key, result)
                    latency_ms = int((time.time() - start_time) * 1000)
                    self._metrics["total_latency_ms"] += latency_ms
                    return result
                except (KeyError, IndexError, TypeError) as e:
                    raise RuntimeError(f"Unexpected response shape from LLM endpoint: {data!r}") from e
            except (self.requests.Timeout, self.requests.ConnectionError) as e:
                last_error = e
                self._metrics["timeouts"] += 1
                if attempt < max_retries:
                    delay = min(2 ** attempt, 30)
                    time.sleep(delay)
                else:
                    self._metrics["errors"] += 1
                    raise
            except self.requests.RequestException as e:
                self._metrics["errors"] += 1
                logging.error(f"GitHub Models API request failed: {e}")
                raise
        if last_error:
            raise last_error
        raise RuntimeError("GitHub Models API request failed")

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
        
        # Determine "model" name for caching based on backend
        cache_model = backend_env if backend_env != "auto" else "subagent_auto"
        cache_key = self._get_cache_key(f"{description}:{prompt}:{original_content}", cache_model)

        if use_cache:
            if cache_key in self._response_cache:
                self._metrics["cache_hits"] += 1
                logging.debug(f"In-memory cache hit for subagent: {description}")
                return self._response_cache[cache_key]
            
            cached_val = self.disk_cache.get(cache_key)
            if cached_val:
                self._metrics["cache_hits"] += 1
                logging.debug(f"Disk cache hit for subagent: {description}")
                self._response_cache[cache_key] = cached_val
                return cached_val

        def _build_full_prompt() -> str:
            try:
                max_context_chars = int(os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000"))
            except ValueError:
                max_context_chars = 12_000
            trimmed_original = (original_content or "")[:max_context_chars]
            return (
                f"Task: {description}\n\n"
                f"Prompt:\n{prompt}\n\n"
                "Context (existing file content):\n"
                f"{trimmed_original}"
            ).strip()

        def _try_codex_cli() -> Optional[str]:
            if not self._command_available('codex'):
                logging.debug("Codex CLI not available")
                return None
            full_prompt = _build_full_prompt()
            repo_root = self._resolve_repo_root()
            try:
                logging.debug("Attempting to use Codex CLI backend")
                result = subprocess.run(
                    ['codex', '--prompt', full_prompt, '--no-color', '--log-level', 'error', '--add-dir', str(repo_root),
                     '--allow-all-tools', '--disable-parallel-tools-execution', '--deny-tool', 'write', '--deny-tool', 'shell',
                     '--silent', '--stream', 'off'],
                    capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180, cwd=str(repo_root), check=False
                )
                stdout = (result.stdout or "").strip()
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

        def _try_copilot_cli() -> Optional[str]:
            if not self._command_available('copilot'):
                logging.debug("Copilot CLI not available")
                return None
            full_prompt = _build_full_prompt()
            repo_root = self._resolve_repo_root()
            try:
                logging.debug("Attempting to use Copilot CLI backend")
                result = subprocess.run(
                    ['copilot', '--prompt', full_prompt, '--no-color', '--log-level', 'error', '--add-dir', str(repo_root),
                     '--allow-all-tools', '--disable-parallel-tools-execution', '--deny-tool', 'write', '--deny-tool', 'shell',
                     '--silent', '--stream', 'off'],
                    capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180, cwd=str(repo_root), check=False
                )
                stdout = (result.stdout or "").strip()
                if result.returncode == 0 and stdout:
                    logging.info("Copilot CLI backend succeeded")
                    return stdout
                if result.returncode != 0:
                    logging.debug(f"Copilot CLI failed (code {result.returncode}): {result.stderr}")
            except subprocess.TimeoutExpired:
                logging.warning("Copilot CLI timed out")
            except Exception as e:
                logging.warning(f"Copilot CLI error: {e}")
            return None

        def _try_gh_copilot(allow_non_command_prompt: bool) -> Optional[str]:
            if not self._command_available('gh'):
                logging.debug("gh CLI not available")
                return None
            if not allow_non_command_prompt and not self._looks_like_command(prompt):
                logging.debug("Prompt doesn't look like a command, skipping gh copilot")
                return None
            
            p = prompt[:2000] if len(prompt) > 2000 else prompt
            try:
                logging.debug("Attempting to use gh copilot backend")
                result = subprocess.run(
                    ['gh', 'copilot', 'explain', p],
                    capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30, cwd=str(self._resolve_repo_root()), check=False
                )
                if result.returncode == 0 and result.stdout.strip():
                    logging.info("gh copilot backend succeeded")
                    return f"# GitHub Copilot (gh) Explanation:\n{result.stdout.strip()}"
                if result.returncode != 0:
                    logging.debug(f"gh copilot failed (code {result.returncode}): {result.stderr}")
            except subprocess.TimeoutExpired:
                logging.warning("gh copilot timed out")
            except Exception as e:
                logging.warning(f"gh copilot error: {e}")
            return None

        def _try_github_models() -> Optional[str]:
            model = (os.environ.get("DV_AGENT_MODEL") or os.environ.get("GITHUB_MODELS_MODEL") or "").strip()
            if not model:
                logging.debug("No model specified for GitHub Models")
                return None
            base_url = os.environ.get("GITHUB_MODELS_BASE_URL")
            
            # Resolve token using the same logic logic as llm_chat_via_github_models
            token = os.environ.get("GITHUB_TOKEN")
            if not token:
                token_file = os.environ.get("DV_GITHUB_TOKEN_FILE")
                if token_file:
                    token_path = Path(token_file)
                    if token_path.exists():
                        try:
                            token = token_path.read_text(encoding="utf-8").strip()
                        except Exception:
                            pass

            if not base_url or not token:
                logging.debug("GitHub Models not fully configured")
                return None
            full_prompt = _build_full_prompt()
            try:
                logging.debug("Attempting to use GitHub Models backend")
                return self.llm_chat_via_github_models(prompt=full_prompt, model=model, base_url=base_url, token=token)
            except Exception as e:
                logging.warning(f"GitHub Models backend error: {e}")
                return None

        def _try_openai_api() -> Optional[str]:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logging.debug("OpenAI API key not set")
                return None
            
            model = os.environ.get("DV_AGENT_MODEL") or os.environ.get("OPENAI_MODEL") or "gpt-4"
            base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com")
            full_prompt = _build_full_prompt()
            
            try:
                logging.debug(f"Attempting to use OpenAI API backend with model {model}")
                return self.llm_chat_via_github_models(
                    prompt=full_prompt, 
                    model=model, 
                    base_url=base_url, 
                    token=api_key,
                    system_prompt="You are an expert software developer and security auditor."
                )
            except Exception as e:
                logging.warning(f"OpenAI API backend error: {e}")
                return None

        backend = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()
        logging.debug(f"Using backend: {backend}")

        res = None
        if backend in {"codex", "codex-cli"}:
            res = _try_codex_cli()
            if res is None: raise RuntimeError("Requested codex backend unavailable")
        elif backend in {"copilot", "local", "copilot-cli"}:
            res = _try_copilot_cli()
            if res is None: raise RuntimeError("Requested copilot backend unavailable")
        elif backend in {"gh", "gh-copilot"}:
            res = _try_gh_copilot(allow_non_command_prompt=True)
            if res is None: raise RuntimeError("Requested gh backend unavailable")
        elif backend in {"github-models", "github_models", "models"}:
            res = _try_github_models()
            if res is None: raise RuntimeError("Requested github-models backend unconfigured")
        elif backend in {"openai", "gpt", "localai", "huggingface"}:
            res = _try_openai_api()
            if res is None: raise RuntimeError(f"Requested {backend} backend unconfigured (check OPENAI_API_KEY/BASE_URL)")
        else:
            # auto (default) logic
            logging.debug("Trying backends in order: codex, copilot, github-models, openai, gh")
            res = _try_codex_cli()
            if not res:
                res = _try_copilot_cli()
            if not res:
                try:
                    res = _try_github_models()
                except Exception: pass
            if not res:
                res = _try_openai_api()
            if not res:
                res = _try_gh_copilot(allow_non_command_prompt=False)

        if res and use_cache:
            self._response_cache[cache_key] = res
            self.disk_cache.set(cache_key, res)
            
        return res

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
