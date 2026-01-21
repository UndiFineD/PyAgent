#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Apache 2.0 License

from __future__ import annotations
from src.core.base.version import VERSION
from .agent_strategy import AgentStrategy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION


class DirectStrategy(AgentStrategy):
    """Standard Zero-Shot strategy: Prompt -> Response."""

    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: str | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        full_prompt = f"{prompt}\n\nContext:\n{context}"
        return await backend_call(full_prompt, system_prompt, history)
