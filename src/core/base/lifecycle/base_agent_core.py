#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""BaseAgentCore - Pure logic and calculation methods for agent operations.

Modularized via the 'core_logic' subpackage to maintain <500 line limit.
"""

from __future__ import annotations
import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Callable
from src.core.base.common.models import (
    AgentConfig,
    ResponseQuality,
    AgentPriority,
    ConversationMessage,
    EventType,
)

# Phase 317: Modularized Logic Mixins
from src.core.base.logic.core import (
    ValidationCore,
    MetricsCore,
    FormattingCore,
    UtilsCore,
    EventCore,
)

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)


class BaseAgentCore(ValidationCore, MetricsCore, FormattingCore, UtilsCore, EventCore):
    """Pure logic core for agent operations (Rust-convertible).

    Inherits from logic mixins to satisfy the 500-line modularization rule.
    """

    def __init__(self) -> None:
        """Initialize the core logic engine."""
        self.context_pool: Dict[str, Any] = {}

    def fix_markdown_content(self, content: str) -> str:
        """Fix markdown formatting in content (Pure Logic)."""
        return self.fix_markdown(content)

    def prepare_capability_payload(
        self, agent_name: str, capabilities: list[str]
    ) -> dict[str, Any]:
        """Prepare the payload for capability registration."""
        return {"agent": agent_name, "capabilities": capabilities}

    def load_config_from_env(self) -> AgentConfig:
        """Load agent configuration from environment variables (Pure Logic)."""
        return AgentConfig(
            backend=os.environ.get("DV_AGENT_BACKEND", "auto"),
            model=os.environ.get("DV_AGENT_MODEL", ""),
            max_tokens=int(os.environ.get("DV_AGENT_MAX_TOKENS", "4096")),
            temperature=float(os.environ.get("DV_AGENT_TEMPERATURE", "0.7")),
            retry_count=int(os.environ.get("DV_AGENT_RETRY_COUNT", "3")),
            timeout=int(os.environ.get("DV_AGENT_TIMEOUT", "60")),
            cache_enabled=os.environ.get("DV_AGENT_CACHE", "true").lower() == "true",
            token_budget=int(os.environ.get("DV_AGENT_TOKEN_BUDGET", "100000")),
        )

    def process_token_tracking(
        self, input_tokens: int, output_tokens: int, model: str
    ) -> dict[str, Any]:
        """Calculates token tracking update dict."""
        return {"input": input_tokens, "output": output_tokens, "model": model}

    def check_token_budget(
        self, current_usage: int, estimated_tokens: int, budget: int
    ) -> bool:
        """Check if request fits within token budget (Logic)."""
        return (current_usage + estimated_tokens) <= budget

    def get_cache_stats(self, cache: dict[str, Any]) -> dict[str, Any]:
        """Calculate cache stats (Logic)."""
        if not cache:
            return {"entries": 0, "total_hits": 0, "avg_quality": 0.0}
        total_hits = sum(getattr(e, "hit_count", 0) for e in cache.values())
        avg_quality = sum(getattr(e, "quality_score", 0) for e in cache.values()) / len(
            cache
        )
        return {
            "entries": len(cache),
            "total_hits": total_hits,
            "avg_quality": avg_quality,
        }

    def perform_health_check(
        self, backend_status: dict[str, Any], cache_len: int, plugins: list[str]
    ) -> Tuple[bool, dict[str, Any]]:
        """Evaluate health status based on backend and components (Logic)."""
        backend_available = any(
            v.get("available", False)
            for v in backend_status.values()
            if isinstance(v, dict)
        )
        details = {
            "backends": backend_status,
            "cache_entries": cache_len,
            "plugins": plugins,
        }
        return backend_available, details

    def collect_tools(self, agent: Any) -> List[Tuple[Callable, str, int]]:
        """Scans agent for methods decorated with @as_tool (Logic only)."""
        import inspect

        collected = []
        for _, method in inspect.getmembers(agent, predicate=inspect.ismethod):
            if hasattr(method, "_is_tool") and method._is_tool:
                category: str = agent.__class__.__name__.replace("Agent", "").lower()
                if hasattr(method, "_tool_category"):
                    category = method._tool_category
                priority: int = getattr(method, "_tool_priority", 0)
                collected.append((method, category, priority))
        return collected

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities list."""
        return ["base", "calculation", "verification"]

    def prepare_improvement_prompt(
        self,
        prompt: str,
        memory_docs: list[str],
        history: list[ConversationMessage],
        system_prompt: str,
    ) -> str:
        """Logic to prepare the final prompt with memory and history."""
        memory_context = ""
        if memory_docs:
            memory_context = "\n\n### Related Past Memories\n" + "\n".join(memory_docs)

        return (
            self.build_prompt_with_history(prompt, history, system_prompt)
            + memory_context
        )

    def finalize_improvement(
        self, improvement: str, post_processors: list[Callable[[str], str]]
    ) -> str:
        """Apply post-processors to improvement string."""
        for processor in post_processors:
            improvement = processor(improvement)
        return improvement

    def get_fallback_response(self) -> str:
        """Returns the standard fallback response text."""
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub Copilot CLI ('copilot') not found or failed.\n"
            "# Install Copilot CLI: https://github.com/github/copilot-cli\n"
            "# Windows: winget install GitHub.Copilot\n"
            "# npm: npm install -g @github/copilot\n"
        )

