#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/BaseAgentCore.description.md

# BaseAgentCore

**File**: `src\\core\base\\BaseAgentCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 21 imports  
**Lines**: 166  
**Complexity**: 13 (moderate)

## Overview

BaseAgentCore - Pure logic and calculation methods for agent operations.

Modularized via the 'core_logic' subpackage to maintain <500 line limit.

## Classes (1)

### `BaseAgentCore`

**Inherits from**: ValidationCore, MetricsCore, FormattingCore, UtilsCore, EventCore

Pure logic core for agent operations (Rust-convertible).

Inherits from logic mixins to satisfy the 500-line modularization rule.

**Methods** (13):
- `__init__(self)`
- `fix_markdown_content(self, content)`
- `prepare_capability_payload(self, agent_name, capabilities)`
- `load_config_from_env(self)`
- `process_token_tracking(self, input_tokens, output_tokens, model)`
- `check_token_budget(self, current_usage, estimated_tokens, budget)`
- `get_cache_stats(self, cache)`
- `perform_health_check(self, backend_status, cache_len, plugins)`
- `collect_tools(self, agent)`
- `get_capabilities(self)`
- ... and 3 more methods

## Dependencies

**Imports** (21):
- `__future__.annotations`
- `core_logic.EventCore`
- `core_logic.FormattingCore`
- `core_logic.MetricsCore`
- `core_logic.UtilsCore`
- `core_logic.ValidationCore`
- `inspect`
- `logging`
- `os`
- `rust_core`
- `src.core.base.models.AgentConfig`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.ConversationMessage`
- `src.core.base.models.EventType`
- `src.core.base.models.ResponseQuality`
- ... and 6 more

---
*Auto-generated documentation*
## Source: src-old/core/base/BaseAgentCore.improvements.md

# Improvements for BaseAgentCore

**File**: `src\\core\base\\BaseAgentCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 166 lines (medium)  
**Complexity**: 13 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BaseAgentCore_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""BaseAgentCore - Pure logic and calculation methods for agent operations.

Modularized via the 'core_logic' subpackage to maintain <500 line limit.
"""

import logging
import os
from typing import Any, Callable, Dict, List, Tuple

from src.core.base.models import (
    AgentConfig,
    ConversationMessage,
)

# Phase 317: Modularized Logic Mixins
from .core_logic import (
    EventCore,
    FormattingCore,
    MetricsCore,
    UtilsCore,
    ValidationCore,
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
